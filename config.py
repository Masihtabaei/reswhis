from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    backend : str = 'faster-whisper'
    model_size : str = 'tiny'
    language : str = 'en'
    sampling_rate : int = 16000
    minimum_chunk_size : float = 1.0
    use_voice_activity_controller : bool = False
    use_voice_activity_detection : bool = False