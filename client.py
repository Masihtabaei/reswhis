import asyncio
import websockets
import sounddevice as sd
import numpy as np
import tkinter as tk
from tkinter import scrolledtext, END
import threading

WS_SERVER_URL = "ws://localhost:8000/ws"
SAMPLING_RATE = 16000
CHANNELS = 1
FORMAT = 'int16'
CHUNK_SIZE = 1024

streaming = False
stream_instance = None
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def audio_stream(websocket):
    global streaming, stream_instance
    try:
        update_log("Connected to WebSocket server. Streaming audio...")

        def callback(indata, frames, time, status):
            if status:
                update_log(f"Audio input status: {status}")
            if streaming:
                loop.call_soon_threadsafe(asyncio.create_task, websocket.send(indata.tobytes()))

        stream_instance = sd.InputStream(
            samplerate=SAMPLING_RATE,
            channels=CHANNELS,
            dtype=FORMAT,
            callback=callback,
            blocksize=CHUNK_SIZE,
        )

        with stream_instance:
            while streaming:
                asyncio.sleep(0.1)

    except Exception as e:
        update_log(f"Error: {e}")
    finally:
        update_log("Audio stream thread exited.")

async def start_websocket():
    global streaming
    try:
        async with websockets.connect(WS_SERVER_URL) as websocket:
            await audio_stream(websocket)
    except Exception as e:
        update_log(f"WebSocket error: {e}")
        streaming = False

def start_streaming():
    global streaming
    if not streaming:
        streaming = True
        threading.Thread(target=loop.run_until_complete, args=(start_websocket(),), daemon=True).start()

def restart():
    text_area.delete('1.0', END)

def update_log(message):
    text_area.insert(tk.END, message + "\n")
    text_area.yview(tk.END)

root = tk.Tk()
root.title("WebSocket Audio Streamer")
root.geometry("400x300")

tk.Label(root, text="Audio Streaming Client", font=("Arial", 14)).pack(pady=5)

start_btn = tk.Button(root, text="Start Streaming", command=start_streaming, bg="green", fg="white")
start_btn.pack(pady=5)

restart_btn = tk.Button(root, text="Restart", command=restart, bg="blue", fg="white")
restart_btn.pack(pady=5)

text_area = scrolledtext.ScrolledText(root, height=300, width=400)
text_area.pack(pady=10)

root.mainloop()
