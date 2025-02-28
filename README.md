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

Requirements for the **faster-whisper** backend (recommended for systems engaging Nvidia GPUs):

1. NVIDIA CUDA Toolkit ([version 12.6 Update 3](https://developer.nvidia.com/cuda-downloads) was tested)
2. NVIDIA cuDNN Library ([version 9.6.0](https://developer.nvidia.com/cudnn-downloads) was tested)


Requirements for the **whisper-timestamped** backend: Nothing! We took care of all for you.

<!--- Requirements for using [Whisper MLX](https://github.com/ml-explore/mlx-examples/tree/main/whisper) as backend:

1. For sure being priviliged to have one of Steve Job's creations (no offense for sure, just for fun :wink:)
2. Running the following command in the project's main directory (as an intermediate step between the second and third steps mentioned in the **usage** subsection):
```
uv add mlx-whisper
```
-->

Requirements for the **openai-whisper** backend:
1. An API key from OpenAI

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
4. Open following file in the code editor of your choice:
```
run.bat
```
5. Change the configurations as needed and save the file (more info in the `configuration` subsection).
6. Double click on the run.bat:
```
run.bat
```

**Important:**
You can also run the server on a machine using **Linux** or **Mac** without the batch file. You first need to set the following environment variables (the exact commands depend on the operating system and the exact values depend on your use case [for more info please refer to the `configuration` subsection]):
```
BACKEND=<value>
MODEL_SIZE=<value>
LANGUAGE=<value>
SAMPLING_RATE=16000 # Fix value (DO NOT CHANGE)
MINIMUM_CHUNK_SIZE=<value>
USE_VOICE_ACTIVITY_CONTROLLER=<value>
USE_VOICE_ACTIVITY_DETECTION=<value>
```

The you can run the server directly as follows:
```
uv run uvicorn main:app
```

7. Open the browser of your choice and head to the following address or send a GET HTTP-request to this endpoint using for e. g. [curl](https://curl.se/), [Wget](https://www.gnu.org/software/wget/) or [Postman](https://www.postman.com/):
```
protocol://ip:port/info
```
**Important**: This REST-endpoint can be used for pinging the server and checking the compatibility of configurations used and specified. If you run the server without changing the default configurations locally and also the port number 8000 is not otherweise bounded, you can use this address:
```
http://localhost:8000/info
```
Hurra :fire:! Now you are officially done! You have three options for using this server:

1. Web-based client
2. Console-based client
3. Custom client

For the web-based client:

1. Change the directory
```
cd clients
```
1. Head to the webpage by opening the following `html` file:
```
web_client.html
```
---

For the console-based client:

1. Run the following command to find out name of the microphone you want to use:
```
ffmpeg -list_devices true -f dshow -i dummy
```
2. Use the following command with the microphone's name replaced to start the transcription:
```
ffmpeg -loglevel debug -f dshow -i audio="<microphone-name>" -ac 1 -ar 16000 -f s16le - | websocat.x86_64-pc-windows-gnu --binary -n ws://localhost:8000/transcribe
```
---

For your custom client:

Fill free to use the language, framework or library of choise. However, following points **must** be considered:

1. Default sampling rate is 16000 (16 kHz).
2. Audio should be mono channel.
3. Data must be transferred as signed 16-bit integer low endian.
4. `/info` is an REST-endpoint and `/transcribe` is a Websocket on.e


## Configurations

You can find and modify the following configurations inside the batch file:

1. `BACKEND`
```
faster-whisper, whisper-timestamped, openai-whisper
```

2. `MODEL_SIZE`
```
tiny.en, tiny, base.en, base, small.en, small, medium.en, medium, large-v1, large-v2, large-v3, large, large-v3-turbo
```

3. `LANGUAGE`
```
af, am, ar, as, az, ba, be, bg, bn, bo, br, bs, ca, cs, cy, da, de, el, en, es, et, eu, fa, fi, fo, fr, gl, gu, ha, haw, he, hi, hr, ht, hu, hy, id, is, it, ja, jw, ka, kk, km, kn, ko, la, lb, ln, lo, lt, lv, mg, mi, mk, ml, mn, mr, ms, mt, my, ne, nl, nn, no, oc, pa, pl, ps, pt, ro, ru, sa, sd, si, sk, sl, sn, so, sq, sr, su, sv, sw, ta, te, tg, th, tk, tl, tr, tt, uk, ur, uz, vi, yi, yo, zh
```
4. `SAMPLING_RATE` (can NOT be modified currently)
5. `MINIMUM_CHUNK_SIZE` $\in \mathbb{N}$ (exlcusive Zero)
6. `USE_VOICE_ACTIVITY_CONTROLLER` $\in \{True, False\}$
7. `USE_VOICE_ACTIVITY_DETECTION` $\in \{True, False\}$

**Important:** we recommend the the `MODEL_SIZE=medium` for transcribing audios spoken in the German language.

## Possible Problems

Here you can find a list of known errors that we experienced with solutions to fix them. Please note that these are issues that are out of our control (e. g. some 3rd-party propreitary dependencies) and we came up with some custom workarounds.

1. ``Could not locate cudnn_ops64_9.dll. Please make sure it is in your library path!Invalid handle. Cannot load symbol cudnnCreateTensorDescriptor``
We experienced this problem on machines using **Microsoft Windows**. First stop the server (for example by using CTRL + C). Please run then the ``copy_cuda_dlls.bat`` as **administrator**. It will prompt you about copying required DLLs so that you can get the problem fixed. After that you can go back to **step number 5** and continue from there. If you installed the NVIDIA CUDA Toolkit and NVIDIA cuDNN Library in a correct manner and also supported version then it should fix the problem.

## Acknowledgement

This project was inspired by:

- https://github.com/ufal/whisper_streaming
- https://github.com/QuentinFuxa/whisper_streaming_web

And employed code from:
- https://github.com/ufal/whisper_streaming (heavily in use)
- https://github.com/snakers4/silero-vad

## License

This project is licensed under [MIT][0].


[0]: https://github.com/Masihtabaei/reswhis/blob/main/LICENSE
