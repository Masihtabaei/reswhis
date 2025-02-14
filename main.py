from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket
import whisper_online
import numpy as np
import logging
import librosa
import soundfile
import io
import sys


SAMPLING_RATE = 16000
MIN_CHUNK = 1.0
IS_FIRST = False

async def receive_audio_chunk(websocket: WebSocket):
    ''' receive_audio_chunk '''
    # receive all audio that is available by this time
    # blocks operation if less than self.min_chunk seconds is available
    # unblocks if connection is closed or a chunk is available
    out = []
    minlimit = MIN_CHUNK * SAMPLING_RATE
    while sum(len(x) for x in out) < minlimit:
        raw_bytes = await websocket.receive_bytes()
        print(raw_bytes)
        if not raw_bytes:
            print('Not raw_bytes')
#           print("received audio:",len(raw_bytes), "bytes", raw_bytes[:10])
        sf = soundfile.SoundFile(io.BytesIO(raw_bytes), channels=1, endian="LITTLE", samplerate=SAMPLING_RATE, subtype="PCM_16", format="RAW")
        audio, _ = librosa.load(sf, sr=SAMPLING_RATE, dtype=np.float32)
        print(out)
        out.append(audio)
    if not out:
        #return None
        print('None')
    conc = np.concatenate(out)
    if IS_FIRST and len(conc) < minlimit:
        #return None
        print('None')
    IS_FIRST.is_first = False
    # return np.concatenate(out)
    print(np.concatenate(out))

def initialize_faster_whisper_tiny_model(app: FastAPI):
    ''' initialize_faster_whisper_tiny_model '''
    app.state.model = dict()
    model = whisper_online.FasterWhisperASR('en', 'tiny')
    app.state.model['faster-whisper-en-tiny'] = model
    app.state.logger.info('Tiny model of faster Whisper loaded successfully!')
    warump_file = whisper_online.load_audio_chunk('./resources/samples_jfk.wav', 0, 1)
    model.transcribe(warump_file)
    app.state.logger.info('Tiny model of faster Whisper warmed up successfully!')

def configure_logger(app: FastAPI):
    ''' configure_logger '''
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler('info.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    app.state.logger = logger
    app.state.logger.info('Logger configured successfully!')

@asynccontextmanager
async def lifespan(app: FastAPI):
    ''' lifespan '''
    configure_logger(app)
    initialize_faster_whisper_tiny_model(app)

    app.state.logger.info('Application startup completed!')
    yield
    app.state.logger.info('Application shutdown process completed!')

app = FastAPI(lifespan=lifespan)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    ''' websocket_endpoint '''
    await websocket.accept()
    while True:
        await receive_audio_chunk(websocket=websocket)
        #await websocket.send_text("You sent nothing!")