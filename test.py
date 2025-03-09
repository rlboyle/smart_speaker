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
                        You are an embedded system running on a raspberry pi 4 with 4GB of ram and raspberry pi OS. You were written in python.
                        you are connected to a speaker and a microphone. You are connected to the internet.
                        You were created for a senior design capstone project by Ryan Boyle, Anna Murray, and Victoria Brown at Northwestern University.
                        You assist me by answering my questions and are always positive. Be concise and accurate with you answers.""",
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

# Replace with your actual device path
device_path = "/dev/input/event2"  # Change to your keyboard event

# Open the input device
device = InputDevice(device_path)

key_pressed = True

# Define the callback function
recorder = Recorder()
def on_key(event, key_pressed):
    if event.type == ecodes.EV_KEY and event.value == 1:  # Key press event
        key_event = categorize(event)
        # print(f"Key pressed: {key_event.keycode}")  # Print the key name
        key_pressed = True
        recorder.start_recording()
        
    if event.type == ecodes.EV_KEY and event.value == 0 and key_pressed:  # Key press event
        key_event = categorize(event)
        # print(f"Key released: {key_event.keycode}")  # Print the key name
        key_pressed = False
        recorder.stop_recording()

# Listen for events and trigger the callback
print(f"Listening for key presses on {device_path}...")
print("Hold the PTT key to talk to Garth")
for event in device.read_loop():
    on_key(event, key_pressed)
    
