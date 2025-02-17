import io
import sys
import logging
from contextlib import asynccontextmanager
import numpy as np
import librosa
import soundfile
from fastapi import FastAPI, WebSocket
import whisper_online
from config import settings


SAMPLING_RATE = 16000
MIN_CHUNK = 1.0
IS_FIRST = True
async def receive_audio_chunk(websocket: WebSocket):
    ''' receive_audio_chunk '''
    # receive all audio that is available by this time
    # blocks operation if less than self.min_chunk seconds is available
    # unblocks if connection is closed or a chunk is available
    global IS_FIRST
    out = []
    minlimit = MIN_CHUNK * SAMPLING_RATE
    while sum(len(x) for x in out) < minlimit:
        raw_bytes = await websocket.receive_bytes()
        await websocket.send_text("Ack!")
        if not raw_bytes:
            break
        #print("received audio:",len(raw_bytes), "bytes", raw_bytes[:10])
        sf = soundfile.SoundFile(io.BytesIO(raw_bytes), channels=1, endian="LITTLE", samplerate=SAMPLING_RATE, subtype="PCM_16", format="RAW")
        audio, _ = librosa.load(sf, sr=SAMPLING_RATE, dtype=np.float32)
        out.append(audio)
    #print("out is full!")
    #output_audio = np.concatenate(out)  # Merge all chunks into one array
    #soundfile.write(f"output-{i}.wav", output_audio, SAMPLING_RATE, subtype="PCM_16")
    #i += 1
    if not out:
        return None
        #print('None')
    conc = np.concatenate(out)
    if IS_FIRST and len(conc) < minlimit:
        return None
    #    print('None')
    IS_FIRST = False
    return np.concatenate(out)
    #print(np.concatenate(out))

def initialize_faster_whisper_tiny_model(instance: FastAPI):
    ''' initialize_faster_whisper_tiny_model '''
    instance.state.model = dict()
    model = whisper_online.FasterWhisperASR('en', 'tiny')
    instance.state.model['faster-whisper-en-tiny'] = model
    instance.state.logger.info('Tiny model of faster Whisper loaded successfully!')
    warump_file = whisper_online.load_audio_chunk('./resources/samples_jfk.wav', 0, 1)
    model.transcribe(warump_file)
    instance.state.logger.info('Tiny model of faster Whisper warmed up successfully!')
    online = whisper_online.OnlineASRProcessor(model)
    instance.state.model['faster-whisper-en-tiny-online'] = online
    instance.state.logger.info('Tiny online transcriber of faster Whisper up and running!')

def configure_logger(instance: FastAPI):
    ''' configure_logger '''
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler('debug.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    instance.state.logger = logger
    instance.state.logger.info('Logger configured successfully!')

@asynccontextmanager
async def lifespan(instance: FastAPI):
    ''' lifespan '''
    configure_logger(app)
    initialize_faster_whisper_tiny_model(app)
    instance.state.logger.info('Application startup completed!')
    yield
    instance.state.logger.info('Application shutdown process completed!')


app = FastAPI(lifespan=lifespan)

@app.get('/info')
async def info():
    return {
        'backend': settings.backend,
        'model_size': settings.model_size,
        'language': settings.language,
        'sampling_rate': settings.sampling_rate,
        'minimum_chunk_size': settings.minimum_chunk_size
    }

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    ''' websocket_endpoint '''
    await websocket.accept()
    app.state.model['faster-whisper-en-tiny-online'].init()
    print("Accepted")
    while True:
        a = await receive_audio_chunk(websocket=websocket)
        if a is None:
            break
        app.state.model['faster-whisper-en-tiny-online'].insert_audio_chunk(a)
        o = app.state.model['faster-whisper-en-tiny-online'].process_iter()
        print(o)
