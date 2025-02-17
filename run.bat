set BACKEDN=faster-whisper
set MODEL_SIZE=large
set LANGUAGE=en
set SAMPLING_RATE=16000
set MINIMUM_CHUNK_SIZE=2.0
uv run uvicorn main:app --reload