set BACKEND=faster-whisper
set MODEL_SIZE=large
set LANGUAGE=en
set SAMPLING_RATE=16000
set MINIMUM_CHUNK_SIZE=1.0
uv run uvicorn main:app --reload