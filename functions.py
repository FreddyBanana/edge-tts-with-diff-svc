from utils.hparams import hparams
import numpy as np
import librosa
import io
import time
from pathlib import Path
import soundfile
from infer_tools import infer_tool
from infer_tools import slicer
import asyncio
import edge_tts #version 6.1.3

chunks_dict = infer_tool.read_temp("./infer_tools/new_chunks_temp.json")

def run_clip(svc_model, key, acc, use_pe, use_crepe, thre, use_gt_mel, add_noise_step, project_name='', f_name=None,
             file_path=None, out_path=None, slice_db=-40, **kwargs):

    print(f'code version:2022-12-04')
    use_pe = use_pe if hparams['audio_sample_rate'] == 24000 else False
    if file_path is None:
        raw_audio_path = f"./raw/{f_name}"
        clean_name = f_name[:-4]
    else:
        raw_audio_path = file_path
        clean_name = str(Path(file_path).name)[:-4]
    infer_tool.format_wav(raw_audio_path)
    wav_path = Path(raw_audio_path).with_suffix('.wav')
    global chunks_dict
    audio, sr = librosa.load(wav_path, mono=True, sr=None)
    wav_hash = infer_tool.get_md5(audio)
    if wav_hash in chunks_dict.keys():
        print("load chunks from temp")
        chunks = chunks_dict[wav_hash]["chunks"]
    else:
        chunks = slicer.cut(wav_path, db_thresh=slice_db)
    chunks_dict[wav_hash] = {"chunks": chunks, "time": int(time.time())}
    infer_tool.write_temp("./infer_tools/new_chunks_temp.json", chunks_dict)
    audio_data, audio_sr = slicer.chunks2audio(wav_path, chunks)

    count = 0
    f0_tst = []
    f0_pred = []
    audio = []
    for (slice_tag, data) in audio_data:
        print(f'#=====segment start, {round(len(data) / audio_sr, 3)}s======')
        length = int(np.ceil(len(data) / audio_sr * hparams['audio_sample_rate']))
        raw_path = io.BytesIO()
        soundfile.write(raw_path, data, audio_sr, format="wav")
        if hparams['debug']:
            print(np.mean(data), np.var(data))
        raw_path.seek(0)
        if slice_tag:
            print('jump empty segment')
            _f0_tst, _f0_pred, _audio = (
                np.zeros(int(np.ceil(length / hparams['hop_size']))),
                np.zeros(int(np.ceil(length / hparams['hop_size']))),
                np.zeros(length))
        else:
            _f0_tst, _f0_pred, _audio = svc_model.infer(raw_path, key=key, acc=acc, use_pe=use_pe, use_crepe=use_crepe,
                                                        thre=thre, use_gt_mel=use_gt_mel, add_noise_step=add_noise_step)
        fix_audio = np.zeros(length)
        fix_audio[:] = np.mean(_audio)
        fix_audio[:len(_audio)] = _audio[0 if len(_audio) < len(fix_audio) else len(_audio) - len(fix_audio):]
        f0_tst.extend(_f0_tst)
        f0_pred.extend(_f0_pred)
        audio.extend(list(fix_audio))
        count += 1
    soundfile.write(out_path, audio, hparams["audio_sample_rate"], 'PCM_16', format=out_path.split('.')[-1])
    return np.array(f0_tst), np.array(f0_pred), audio


async def _main(text, voice, output_file) -> None:
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)


def generate_wav(text, voice, output_file):
    asyncio.get_event_loop().run_until_complete(_main(text, voice, output_file))

