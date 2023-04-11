import os
from functions import generate_wav, run_clip
from infer_tools.infer_tool import Svc
import logging

# Modifiable
TEXT_INPUT_PATH = "./text.txt"  # Path of text to be converted
VOICE = "zh-CN-XiaoyiNeural"  # You can change the available voice here
OUTPUT_NAME = "output"  # Name of the output file
PROJECT_NAME = "project"  # Project name used during diff-svc training
MODEL_PATH = "./model_ckpt_steps_48000.ckpt"  # Model path
CONFIG_PATH = "./config.yaml"  # Model config path, correspond to the model

# Unmodifiable
OUTPUT_PATH = "./output_tts/"

if __name__ == "__main__":
    logging.getLogger('numba').setLevel(logging.WARNING)

    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    text = open(TEXT_INPUT_PATH, encoding="utf-8")
    lines = text.readlines()  # Line feed means segmentation, each segment generates an audio file
    for i, line in enumerate(lines):
        output_file = OUTPUT_PATH + OUTPUT_NAME + "_ori_" + str(i) + ".wav"
        generate_wav(line, VOICE, output_file)

    hubert_gpu = True
    svc_model = Svc(PROJECT_NAME, CONFIG_PATH, hubert_gpu, MODEL_PATH)
    print('model loaded')

    for i in range(len(lines)):
        input_wav_file = OUTPUT_PATH + OUTPUT_NAME + "_ori_" + str(i) + ".wav"
        while not os.path.exists(input_wav_file):
            print("Waiting for file generation")
        wav_gen = OUTPUT_PATH + OUTPUT_NAME + "_target_" + str(i) + ".wav"
        f0_tst, f0_pred, audio = run_clip(svc_model, file_path=input_wav_file, key=0, acc=20, use_crepe=False,
                                          use_pe=False, thre=0.05, use_gt_mel=False, add_noise_step=300,
                                          project_name=PROJECT_NAME, out_path=wav_gen)
