#!/bin/sh
export BACKEND=faster-whisper
export MODEL_SIZE=tiny
export LANGUAGE=en
export SAMPLING_RATE=16000  # DO NOT CHANGE
export MINIMUM_CHUNK_SIZE=1.0
export USE_VOICE_ACTIVITY_CONTROLLER=False
export USE_VOICE_ACTIVITY_DETECTION=False

uv run uvicorn main:app