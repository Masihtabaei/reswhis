set BACKEND=faster-whisper
set MODEL_SIZE=tiny
set LANGUAGE=en
set SAMPLING_RATE=16000
set MINIMUM_CHUNK_SIZE=1.0
set USE_VOICE_ACTIVITY_CONTROLLER=False
uv run uvicorn main:app --reload