import io
import sys
import logging
from contextlib import asynccontextmanager
import numpy as np
import librosa
import soundfile
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import whisper_online
from config import Settings


class Worker:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.is_first = True
        self.transcriber = whisper_online.OnlineASRProcessor(websocket.app.state.model)
        websocket.app.state.logger.info('Transcriber initialized successfully!')

    async def receive_audio_chunk(self):
        ''' receive_audio_chunk '''
        sampling_rate = self.websocket.app.state.settings.sampling_rate
        out = []
        lower_bound = self.websocket.app.state.settings.minimum_chunk_size * sampling_rate
        while sum(len(x) for x in out) < lower_bound:
            raw_bytes = await self.websocket.receive_bytes()
            await self.websocket.send_text("ACK")
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
        if self.is_first and len(conc) < lower_bound:
            return None
        
        self.is_first = False
        return np.concatenate(out)

    async def run(self):
        try:
            while True:
                a = await self.receive_audio_chunk()
                if a is None:
                    break
                self.transcriber.insert_audio_chunk(a)
                o = self.transcriber.process_iter()
                print(o)
        except WebSocketDisconnect:
            self.websocket.app.state.logger.info('Connection closed!')

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
    worker = Worker(websocket)
    app.state.logger.info('Connection established successfully!')
    await worker.run()