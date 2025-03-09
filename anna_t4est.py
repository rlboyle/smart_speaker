import os
import wave
import pyaudio
import pyttsx3
import whisper
from anthropic import Anthropic
from dotenv import load_dotenv

# --- Evdev imports ---
from evdev import InputDevice, categorize, ecodes

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class Recorder:
    def __init__(self, client):
        self.client = client
        self.recording = False
        self.p = pyaudio.PyAudio()
        self.model = whisper.load_model("tiny")
        self.messages = []
        self.stream = None
        self.frames = []
        self.engine = pyttsx3.init()

    def start_recording(self):
        if self.recording:
            return
        self.frames = []
        self.recording = True
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            stream_callback=self.callback
        )
        print("Recording...")

    def stop_recording(self):
        if not self.recording:
            return
        self.stream.stop_stream()
        self.stream.close()
        print("Finished recording.")
        self.recording = False

        # Save recorded audio to disk
        with wave.open("input.wav", "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(self.frames))

        # Transcribe with Whisper
        result = self.model.transcribe("input.wav", fp16=False)
        text = result["text"].strip()

        # If there's transcribed text, send to Anthropic and TTS
        if text:
            self.messages.append({"role": "user", "content": text})
            message = self.client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=256,
                system="""
                    You are a helpful smart speaker assistant prototype named Garth.
                    You are an embedded system running on a raspberry pi 4 with 4GB of ram and raspberry pi OS.
                    You were created for a senior design capstone project at Northwestern University.
                    You assist me by answering my questions, always positive, concise, and accurate.
                """,
                messages=self.messages
            )

            self.text_to_speech(message.content[0].text)
            self.messages.append({"role": "assistant", "content": message.content[0].text})

            # Truncate conversation if it gets too long
            if len(self.messages) > 8:
                self.messages.pop(0)
        else:
            self.text_to_speech("I didn't catch that. Could you repeat?")

        print("Hold the '1' key to speak to Garth...")

    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return (None, pyaudio.paContinue)

    def text_to_speech(self, text):
        print(text)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[29].id)  # or another valid index
        self.engine.say(text)
        self.engine.runAndWait()   # <-- Use runAndWait() instead of startLoop, iterate, endLoop


if __name__ == "__main__":
    load_dotenv()
    client = Anthropic()
    recorder = Recorder(client=client)

    # Hard-coded path to keyboard device
    keyboard_device = InputDevice("/dev/input/event2")
    print("Hold the '1' key to speak to Garth...")

    try:
        for event in keyboard_device.read_loop():
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
    except KeyboardInterrupt:
        print("Exiting...")
