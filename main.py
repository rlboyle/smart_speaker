from dotenv import load_dotenv
import os
from anthropic import Anthropic
import sys
import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write
import whisper
from gtts import gTTS
import pyttsx3
from pynput import keyboard
import pyaudio
import wave
import whisper

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"

def text_to_speech(text):
    print(text)
    # os.system(f"espeak \"{text}\"")
    # os.system(f"say \"{text}\"") # say works for mac
    # obj = gTTS(text=text, lang='en', slow=False)
    # obj.save("output.mp3")
    # os.system("mpg321 output.mp3") # mpg321 should work for raspberry pi
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[14].id) # change voice
    engine.say(text)
    # engine.runAndWait()
    engine.startLoop(False)
    engine.iterate()
    engine.endLoop()
    print("Hold shift to speak to Garth...")
    
class Recorder:
    def __init__(self):
        self.recording = False
        self.p = pyaudio.PyAudio()
        self.model = whisper.load_model("tiny")

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

        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))

        result = self.model.transcribe("output.wav", fp16=False)
        # print(result["text"])
        message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=256,
                system="""You are a helpful smart speaker assistant named Garth.
                    You assist me by answering my questions and are always positive. Be concise with you answers.""",
                messages=[
                    {"role": "user", "content": result["text"]},
                ]
            )
        text_to_speech(message.content[0].text)
        


    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return (None, pyaudio.paContinue)
    
class Listener(keyboard.Listener):
    def __init__(self, recorder):
        super(Listener, self).__init__(self.on_press, self.on_release)
        self.recorder = recorder

    def on_press(self, key):
        try:
            if key == keyboard.Key.shift:
                self.recorder.start_recording()
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key == keyboard.Key.shift:
                self.recorder.stop_recording()
        except AttributeError:
            pass

if __name__ == "__main__":
    try:
        load_dotenv()
        client = Anthropic()
        print("Hold shift to speak to Garth...")
        recorder = Recorder()
        listener = Listener(recorder)
        listener.start()
        listener.join()

    except KeyboardInterrupt:
        print(f"\nExiting...")
    


