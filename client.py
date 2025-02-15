import asyncio
import websockets
import sounddevice as sd

WS_SERVER_URL = "ws://localhost:8000/ws"
SAMPLING_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1024  # Number of frames per chunk

def audio_callback(indata, frames, time, status):
    '''Test'''
    if status:
        print(f"Audio input status: {status}")
    asyncio.run_coroutine_threadsafe(send_audio(indata), loop)

async def send_audio(indata):
    '''Test'''
    try:
        await websocket.send(indata.tobytes())
    except Exception as e:
        print(f"WebSocket send error: {e}")

async def start_streaming():
    '''Test'''
    global websocket, loop
    loop = asyncio.get_event_loop()
    
    try:
        async with websockets.connect(WS_SERVER_URL) as ws:
            websocket = ws
            with sd.InputStream(samplerate=SAMPLING_RATE, channels=CHANNELS, dtype='int16', callback=audio_callback, blocksize=CHUNK_SIZE):
                print("Streaming started...")
                await asyncio.Future()  # Keep the coroutine running
    except Exception as e:
        print(f"WebSocket error: {e}")

if __name__ == "__main__":
    asyncio.run(start_streaming())
