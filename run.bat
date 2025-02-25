set BACKEND=faster-whisper
set MODEL_SIZE=medium
set LANGUAGE=de
set SAMPLING_RATE=16000
set MINIMUM_CHUNK_SIZE=1.0
set USE_VOICE_ACTIVITY_CONTROLLER=False
set USE_VOICE_ACTIVITY_DETECTION=False
uv run uvicorn main:app --reload