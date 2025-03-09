import evdev
from evdev import InputDevice, categorize, ecodes
import os
from dotenv import load_dotenv
import os
from anthropic import Anthropic
# import sys
# import sounddevice as sd
# import soundfile as sf
# from scipy.io.wavfile import write
import whisper
from gtts import gTTS
import pyttsx3
# from pynput import keyboard
import keyboard

import pyaudio
import wave

import sys

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"

def text_to_speech(text):
    print(text)
    os.system(f"espeak \"{text}\"")

client = Anthropic()

class Recorder:
    def __init__(self):
        self.recording = False
        self.p = pyaudio.PyAudio()
        self.model = whisper.load_model("tiny")
        self.messages = []

    def start_recording(self):
        if self.recording:
            # print("Already recording...")
            return
        self.frames = []
        self.recording = True
        self.stream = self.p.open(format=FORMAT, channels=CHANNELS,
                             rate=RATE, input=True,
                             frames_per_buffer=CHUNK,
                             stream_callback=self.callback)
        print("Recording...")
        self.recording = True

    def stop_recording(self):
        if not self.recording:
            # print("Not recording...")
            return
        self.stream.stop_stream()
        self.stream.close()
        # p.terminate()
        print("Finished recording.")
        self.recording = False

        with wave.open('input.wav', 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))

        result = self.model.transcribe("input.wav", fp16=False)
        # print("sent message: m", result["text"], "m")
        if result["text"] != "" and result["text"] != " ":
            self.messages.append({"role": "user", "content": result["text"]})
            message = client.messages.create(
                    model="claude-3-5-sonnet-latest",
                    max_tokens=256,
                    system="""You are a helpful smart speaker assistant prototype named Garth.
                        You are an embedded system running on a raspberry pi 5 with 4GB of ram and raspberry pi OS. You were written in python.
                        you are connected to a speaker and a microphone. You are connected to the internet.
                        You were created for a senior design capstone project by Ryan Boyle, Anna Murray, and Victoria Brown at Northwestern University.
                        You assist me by answering my questions and are always positive. Be concise and accurate with you answers. Keep in mind that the prompts you
                        are given are translated from a real voice using speech to text software so grammar and syntax may not always be correct.
                        If you don't understand something, ask for clarification. Also remember that your answers will also be fed through a text to speech software, so make sure that you
                        answer as if participating in a live spoken conversation as opposed to a text chat. This means no emojis or numbered lists.""",
                    messages=self.messages
                )
        
            # print(message.content[0].text)
            text_to_speech(message.content[0].text)
            self.messages.append({"role": "assistant", "content": message.content[0].text})
            if len(self.messages) > 8:
                self.messages.pop(0)

        else:
            text_to_speech("I didn't catch that. Could you repeat?")

        print("Hold the PTT key to speak to Garth...")

    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return (None, pyaudio.paContinue)

# Define the callback function
# recorder = Recorder()
def on_key(event):
    if event.type == ecodes.EV_KEY:
                data = categorize(event)
                # If the key is KEY_1
                if data.keycode == "KEY_1":
                    # Pressed down -> start recording
                    if data.keystate == data.key_down:
                        recorder.start_recording()
                    # Released -> stop recording
                    elif data.keystate == data.key_up:
                        recorder.stop_recording()

# Listen for events and trigger the callback
if __name__ == "__main__":
    try:
        recorder = Recorder()
        load_dotenv()
        client = Anthropic()
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        device = None
        print("Searching for PTT button device")
        for d in devices:
            # print(device)
            # print(f"{d.path}: {d.name}")
            if d.name == "SayoDevice SayoDevice nano":
                # Open the input device
                device_path = d.path
                device = InputDevice(device_path)
                print(f"Found {device.name} on path {device_path}")

        if not device:
            print("Unable to find PTT button device")
            sys.exit(1)


        print(f"Listening for key presses on {device_path}...")
        print("Hold the PTT key to talk to Garth")
        # key_pressed = True
        for event in device.read_loop():
            on_key(event)
    except KeyboardInterrupt:
        print("Exiting ...")
    
