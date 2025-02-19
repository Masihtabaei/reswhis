# reswhis

## Status & Tech Stack

[![ruff-Linting](https://github.com/Masihtabaei/reswhis/actions/workflows/ruff.yml/badge.svg)](https://github.com/Masihtabaei/reswhis/actions/workflows/ruff.yml)</br>
![uv Badge](https://img.shields.io/badge/uv-DE5FE9?logo=uv&logoColor=fff&style=flat-square)
![Ruff Badge](https://img.shields.io/badge/Ruff-D7FF64?logo=ruff&logoColor=000&style=flat-square)
![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=flat-square)
![Git Badge](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=fff&style=flat-square)
![GitHub Badge](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=fff&style=flat-square)

## Background

After countless hours of testing various packages, libraries, and frameworks, we realized there was no **remote**, **robust**, **language-agnostic** WebSocket solution for real-time audio transcription using OpenAI’s Whisper. Existing solutions were usually error-prone, restricted to local use or sophisticated.

Inspired by the **stream socket** (i. e. communication over **TCP**) server implementation of "placeholder", we decided to develop our own WebSocket server for Whisper-based streaming transcription.

Main characteristics of our implementation:
- **Simple**: Done merely over a weekend by an undergrad student.
- **Websocket-based**: Broader client support (also possible to integrate into web apps without native socket support)
- **Parallel server**: Simultaneous transcription for multiple clients.

Confused about the name?
Finding cool and innovative names is probably one of the hardest tasks to accomplish. 

## Usage

TBD

## Acknowledgement

TBD

## License

This project is licensed under [MIT][0].


[0]: https://github.com/Masihtabaei/reswhis/blob/main/LICENSE