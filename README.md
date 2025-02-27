# reswhis :studio_microphone:


## Status

[![ruff-Linting](https://github.com/Masihtabaei/reswhis/actions/workflows/ruff.yml/badge.svg)](https://github.com/Masihtabaei/reswhis/actions/workflows/ruff.yml) 
[![uv](https://github.com/Masihtabaei/reswhis/actions/workflows/uv.yml/badge.svg)](https://github.com/Masihtabaei/reswhis/actions/workflows/uv.yml)
</br>

## Tech Stack

![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=flat-square)
![FastAPI Badge](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=fff&style=flat-square)
![uv Badge](https://img.shields.io/badge/uv-DE5FE9?logo=uv&logoColor=fff&style=flat-square)
![Ruff Badge](https://img.shields.io/badge/Ruff-D7FF64?logo=ruff&logoColor=000&style=flat-square)
![Git Badge](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=fff&style=flat-square)
![GitHub Badge](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=fff&style=flat-square)

## Background

After countless hours of testing various packages, libraries, and frameworks, we realized there was no **remote**, **robust**, **language-agnostic** solution for real-time audio transcription using [OpenAI’s Whisper](https://github.com/openai/whisper). Existing solutions were usually error-prone, restricted to local use or not easy to install or integrate.

Inspired by the [stream socket](https://en.wikipedia.org/wiki/Berkeley_sockets) (in a nutshell direct communication over **TCP**) server implementation of [whisper-streaming](https://github.com/ufal/whisper_streaming), we decided to develop our own [Websocket](https://de.wikipedia.org/wiki/WebSocket) server for Whisper-based streaming transcription.

Main characteristics of our implementation:
- :beginner: **Simple**: Done by an undergrad student having simplicity in his head.
- :rocket: **Fast**: Thanks to the FastAPI 
- :globe_with_meridians: **Websocket-based**: Broader client support (also possible to integrate into web apps without native socket support)
- :twisted_rightwards_arrows: **Parallel server**: Capable of handling multiple clients simultaneously.

We all know the struggle of naming a project—it’s almost as hard as the project itself. But every creation deserves a name, and this one is no exception. The name **reswhis** is a blend of **Re**mote **S**treaming **Whis**per. 

## Requirements

**Important**: It worths scrolling down to the end of this page, if you got in trouble installing these two requirements.

General and independent requirements:

1. [uv](https://docs.astral.sh/uv/getting-started/installation/) for managing the project, packages and also dependencies
2. FFmpeg ([2024-12-19-git-494c961379-full_build-www.gyan.dev](https://ffmpeg.org/download.html) was tested)

Requirements for the **faster-whisper** backend:

1. NVIDIA CUDA Toolkit ([version 12.6 Update 3](https://developer.nvidia.com/cuda-downloads) was tested)
2. NVIDIA cuDNN Library ([version 9.6.0](https://developer.nvidia.com/cudnn-downloads) was tested)


Requirements for the **whisper-timestamped** backend:

1. Nothing! We took care of all for you.

Requirements for using [Whisper MLX](https://github.com/ml-explore/mlx-examples/tree/main/whisper) as backend:

1. For sure being priviliged to have one of Steve Job's creations (no offense for sure, just for fun :wink:)
2. Running the following command in the project's main directory (as an intermediate step between the second and third steps mentioned in the **usage** subsection):
```
uv add mlx-whisper
```


Requirements for using our web client for testing (can get ignored if you develop your own client):

1. Browser of your choice
2. A working microphone

Requirements for using our test client on a machine using **Microsoft Windows** as (can get ignored if you use the web client or prefer your own client):

1. websocat ([v1.14.0](https://github.com/vi/websocat/releases/tag/v1.14.0) was tested)
2. A working microphone

## Usage


1. Clone the repository
```
git clone https://github.com/Masihtabaei/reswhis.git
```
2. Change the directory
```
cd reswhis
```
3. Run the uv
```
uv sync
```
4. Click on the run.bat (you can also change the model size, language etc, in this batch file):
```
run.bat
```
5. Open the browser of your choice and head to the following address or send a GET HTTP-request to this endpoint using for e. g. [curl](https://curl.se/), [Wget](https://www.gnu.org/software/wget/) or [Postman](https://www.postman.com/):
```
protocol://ip:port/info
```
**Important**: This REST-endpoint can be used for pinging the server and checking the compatibility of configurations used and specified. If you run the server without changing the default configurations locally and also the port number 8000 is not otherweise bounded, you can use this address:
```
http://localhost:8000/info
```


6. Change the directory
```
cd clients
```
1. Head to the webpage by opening the following `html` file:
```
web_client.html
```


## Possible Problems

Here you can find a list of known errors that we experienced with solutions to fix them. Please note that these are issues that are out of our control (e. g. some 3rd-party propreitary dependencies) and we came up with some custom workarounds.

1. ``Could not locate cudnn_ops64_9.dll. Please make sure it is in your library path!Invalid handle. Cannot load symbol cudnnCreateTensorDescriptor``
We experienced this problem on machines using **Microsoft Windows**. First stop the server (for example by using CTRL + C). Please run then the ``copy_cuda_dlls.bat`` as **administrator**. It will prompt you about copying required DLLs so that you can get the problem fixed. After that you can go back to **step number 5** and continue from there. If you installed the NVIDIA CUDA Toolkit and NVIDIA cuDNN Library in a correct manner and also supported version then it should fix the problem.

## Acknowledgement



## License

This project is licensed under [MIT][0].


[0]: https://github.com/Masihtabaei/reswhis/blob/main/LICENSE
