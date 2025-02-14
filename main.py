from contextlib import asynccontextmanager
from fastapi import FastAPI
import whisper_online
import logging
import sys

def load_faster_whisper_tiny_model(app: FastAPI):
    app.state.whisper_tiny_model = whisper_online.FasterWhisperASR('en', 'tiny')
    app.state.logger.info('Tiny model loaded successfully!')
    
def configure_logger(app: FastAPI):
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
    configure_logger(app)
    load_faster_whisper_tiny_model(app)

    app.state.logger.info('Application startup completed!')
    yield
    app.state.logger.info('Application shutdown process completed!')

app = FastAPI(lifespan=lifespan)