# reswhis

## Status

[![ruff-Linting](https://github.com/Masihtabaei/reswhis/actions/workflows/ruff.yml/badge.svg)](https://github.com/Masihtabaei/reswhis/actions/workflows/ruff.yml)

## General Information

After countless hours of testing various packages, libraries, and frameworks, we realized there was no **remote**, **robust**, **language-agnostic** WebSocket solution for real-time audio transcription using OpenAI’s Whisper. Existing solutions were usually error-prone, restricted to local use or sophisticated.

Inspired by the **stream socket** (i. e. communication over **TCP**) server implementation of "placeholder", we decided to develop our own WebSocket server for Whisper-based streaming transcription.

Main characteristics of our implementation:
- **Simple**: Done merely over a weekend by an undergrad student.
- **Websocket-based**: Broader client support (also possible to integrate into web apps without native socket support)
- **Parallel server**: Simultaneous transcription for multiple clients.


## Tech Stack



## Usage

TBD

## Acknowledgement

TBD

## License

This project is licensed under [MIT][0].


[0]: https://github.com/Masihtabaei/reswhis/blob/main/LICENSE