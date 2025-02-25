# reswhis 

[![ruff-Linting](https://github.com/Masihtabaei/reswhis/actions/workflows/ruff.yml/badge.svg)](https://github.com/Masihtabaei/reswhis/actions/workflows/ruff.yml) 
[![uv](https://github.com/Masihtabaei/reswhis/actions/workflows/uv.yml/badge.svg)](https://github.com/Masihtabaei/reswhis/actions/workflows/uv.yml)
</br>
=======
## A Name Worth Whispering  

We all know the struggle of naming a project—it’s almost as hard as the project itself. But every creation deserves a name, and this one is no exception. Enter **reswhis**—a blend of **Re**mote **S**treaming **Whis**per. Short, sharp, and to the point, just like the seamless speech-to-text magic it enables. A whisper that travels across the web, captured and transcribe in real-time. 


## Tech Stack: Under the Hood

![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=flat-square)
![FastAPI Badge](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=fff&style=flat-square)
![uv Badge](https://img.shields.io/badge/uv-DE5FE9?logo=uv&logoColor=fff&style=flat-square)
![Ruff Badge](https://img.shields.io/badge/Ruff-D7FF64?logo=ruff&logoColor=000&style=flat-square)
![Git Badge](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=fff&style=flat-square)
![GitHub Badge](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=fff&style=flat-square)

## Background: Root of All Evil

After countless hours of testing various packages, libraries, and frameworks, we realized there was no **remote**, **robust**, **language-agnostic** WebSocket solution for real-time audio transcription using OpenAI’s Whisper. Existing solutions were usually error-prone, restricted to local use or sophisticated.

Inspired by the **stream socket** (i. e. direct communication over **TCP**) server implementation of "placeholder", we decided to develop our own WebSocket server for Whisper-based streaming transcription.

Main characteristics of our implementation:
- **Simple**: Done merely over a weekend by an undergrad student.
- **Websocket-based**: Broader client support (also possible to integrate into web apps without native socket support)
- **Parallel server**: Simultaneous transcription for multiple clients.

## Requirements

General and independent requirements:

1. [uv](https://docs.astral.sh/uv/getting-started/installation/) for managing the project, packages and also dependencies

Requirements for the **faster-whisper** backend:

1. NVIDIA CUDA Toolkit ([version 12.6 Update 3](https://developer.nvidia.com/cuda-downloads) was tested)
2. NVIDIA cuDNN Library ([version 9.6.0](https://developer.nvidia.com/cudnn-downloads) was tested)

Requirements for using our test client on a machine using **Microsoft Windows** (can get ignored if you use the web client):

1. FFmpeg ([2024-12-19-git-494c961379-full_build-www.gyan.dev](https://ffmpeg.org/download.html) was tested)
2. websocat ([v1.14.0](https://github.com/vi/websocat/releases/tag/v1.14.0) was tested)
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
4. Click on the run.bat:
```
run.bat
```
5. Head to the webpage by opening the following `html` file:
```
client.html
```

**Important**: There is a REST-endpoint for pinging the server available at the following address:
```
http://localhost:8000/info
```

## Acknowledgement



## License

This project is licensed under [MIT][0].


[0]: https://github.com/Masihtabaei/reswhis/blob/main/LICENSE
