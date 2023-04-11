# Edge-tts with Diff-svc



## 简介 / Introduction

本仓库基于edge-tts与diff-svc，简单实现了文本控制语音生成与音色转换技术的结合。

This repo is based on edge-tts and diff-svc, and realizes the combination of text to speech and singing voice conversion in a simple way.



## 安装依赖 / Installing the dependencies

在diff-svc环境的基础上，只需安装edge-tts。

On the basis of diff-svc environment, only edge-tts needs to be installed.

```
$ pip install edge-tts==6.1.3
```



## 使用方法 / Usage

### step 1

将文件移动至diff-svc仓库主目录下。

Move the files to the main directory of the diff-svc repository.

### step 2

在main.py文件中修改下列参数：

- **TEXT_INPUT_PATH**，存放待转换文本的txt文件路径；
- **VOICE**，edge-tts说话人；
- **OUTPUT_NAME**，输出音频文件的名称；
- **PROJECT_NAME**，diff-svc模型的项目名，务必与训练时的命名相同；
- **MODEL_PATH**，diff-svc模型路径；
- **CONFIG_PATH**，diff-svc模型config路径

Modify the following parameters in main.py: 

- **TEXT_INPUT_PATH**, the path to the txt file that stores the text to be converted; 
- **VOICE**, the edge-tts speaker; 
- **OUTPUT_NAME**, the file name of the output audio;
- **PROJECT_NAME**, the project name of the diff-svc model, must be the same as the project name during training;
- **MODEL_PATH**, the path of the diff-svc model;
- **CONFIG_PATH**, the path of the diff-svc model config.

```python
# Modifiable
TEXT_INPUT_PATH = "./text.txt"  # Path of text to be converted
VOICE = "zh-CN-XiaoyiNeural"  # You can change the available voice here
OUTPUT_NAME = "output"  # Name of the output file
PROJECT_NAME = "project"  # Project name used during diff-svc training
MODEL_PATH = "./model_ckpt_steps_48000.ckpt"  # Model path
CONFIG_PATH = "./config.yaml"  # Model config path, correspond to the model
```

### step 3

在**TEXT_INPUT_PATH**指向的txt文件中填写待转换文本。换行（回车键）代表换段，每段单独生成一个音频文件。

Place the text to be converted in the txt file of **TEXT_INPUT_PATH**. A newline (Enter key) means a new segment, and each segment can generate independent audio.

### step 4

运行main.py文件。

Run main.py.

```
$ python main.py
```



## 其它 / Others

如果音色转换的效果不理想，可以在main.py中修改**run_clip**的参数。具体修改策略请参考diff-svc仓库的教程文档。

If the effect of voice conversion does not meet your expectations, you can modify the parameters of the **run_clip** in the file. For modification strategies, please refer to the tutorial documentation of diff-svc repository.



## 参考 / Reference

[prophesier/diff-svc: Singing Voice Conversion via diffusion model (github.com)](https://github.com/prophesier/diff-svc)

[rany2/edge-tts: Use Microsoft Edge's online text-to-speech service from Python (without needing Microsoft Edge/Windows or an API key) (github.com)](https://github.com/rany2/edge-tts)
