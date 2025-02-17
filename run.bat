export BACKEDN="faster-whisper"
export MODEL_SIZE="large"
uv run uvicorn main:app --reload
