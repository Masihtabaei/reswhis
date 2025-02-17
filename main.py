import io
import sys
import logging
from contextlib import asynccontextmanager
import numpy as np
import librosa
import soundfile
from fastapi import FastAPI, WebSocket
import whisper_online
from config import Settings


IS_FIRST = True

async def receive_audio_chunk(websocket: WebSocket):
    ''' receive_audio_chunk '''
    global IS_FIRST
    sampling_rate = websocket.app.state.settings.sampling_rate
    out = []
    lower_bound = websocket.app.state.settings.minimum_chunk_size * sampling_rate
    while sum(len(x) for x in out) < lower_bound:
        raw_bytes = await websocket.receive_bytes()
        await websocket.send_text("ACK")
        if not raw_bytes:
            break
        sf = soundfile.SoundFile(io.BytesIO(raw_bytes), channels=1, endian="LITTLE", samplerate=sampling_rate, subtype="PCM_16", format="RAW")
        audio, _ = librosa.load(sf, sr=sampling_rate, dtype=np.float32)
        out.append(audio)
    #output_audio = np.concatenate(out)  # Merge all chunks into one array
    #soundfile.write(f"output-{i}.wav", output_audio, SAMPLING_RATE, subtype="PCM_16")
    #i += 1
    if not out:
        return None
    conc = np.concatenate(out)
    if IS_FIRST and len(conc) < lower_bound:
        return None
    
    IS_FIRST = False
    return np.concatenate(out)

def parse_settings(instance: FastAPI):
    app.state.settings = Settings()
    instance.state.logger.info('Settings parsed successfully!')

def load_model(instance: FastAPI):
    ''' Loads the model desired '''
    instance.state.model = whisper_online.FasterWhisperASR(app.state.settings.language, app.state.settings.model_size)
    instance.state.logger.info('Model loaded successfully!')

def warmup_loaded_model(instance: FastAPI):
    ''' Warumups the model loaded '''
    warump_file = whisper_online.load_audio_chunk('./resources/samples_jfk.wav', 0, 1)
    instance.state.model.transcribe(warump_file)
    instance.state.logger.info('Model warmed up successfully!')

def initialize_transcriber(instance: FastAPI):
    ''' Instantiates and initializes a transcriber from the model loaded '''
    instance.state.transcriber = whisper_online.OnlineASRProcessor(instance.state.model)
    instance.state.logger.info('Transcriber initialized successfully!')

def configure_logger(instance: FastAPI):
    ''' Configures the logger '''
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
    ''' Manages the startup and shutdown processes '''
    configure_logger(app)
    parse_settings(app)
    load_model(app)
    warmup_loaded_model(app)
    initialize_transcriber(app)
    instance.state.logger.info('Application startup completed!')
    yield
    instance.state.logger.info('Application shutdown process completed!')


app = FastAPI(lifespan=lifespan)

@app.get('/info')
async def info():
    ''' Serves as a REST-endpoint for service information retrieval '''
    return {
        'backend': app.state.settings.backend,
        'model_size': app.state.settings.model_size,
        'language': app.state.settings.language,
        'sampling_rate': app.state.settings.sampling_rate,
        'minimum_chunk_size': app.state.settings.minimum_chunk_size
    }

@app.websocket('/transcribe')
async def transcribe(websocket: WebSocket):
    ''' Serves as a websocket-endpoint for transcription '''
    await websocket.accept()
    app.state.transcriber.init()
    print("Accepted")
    while True:
        a = await receive_audio_chunk(websocket=websocket)
        if a is None:
            break
        app.state.transcriber.insert_audio_chunk(a)
        o = app.state.transcriber.process_iter()
        print(o)