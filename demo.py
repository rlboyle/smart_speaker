from dotenv import load_dotenv
import os
from anthropic import Anthropic
# import sys
# import sounddevice as sd
# import soundfile as sf
# from scipy.io.wavfile import write
import whisper
# from gtts import gTTS
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

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[14].id) # change voice

def text_to_speech(text):
    print(text)
    # os.system(f"espeak \"{text}\"")
    # os.system(f"say \"{text}\"") # say works for mac
    # obj = gTTS(text=text, lang='en', slow=False)
    # obj.save("output.mp3")
    # os.system("mpg321 output.mp3") # mpg321 should work for raspberry pi

    # engine = pyttsx3.init(driverName='espeak')
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[14].id) # change voice
    os.system("espeak \"{text}\"")
    # engine.save_to_file(text, 'output.wav')
    # os.system("aplay output.wav")
    
    # engine.startLoop(False)
    # engine.iterate()
    # engine.endLoop()
    # tts = TTS()
    # tts.speak(text)
    # del(tts)

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

        print("Hold shift to speak to Garth...")
        


    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return (None, pyaudio.paContinue)
    
# class Listener(keyboard.Listener):
#     def __init__(self, recorder):
#         super(Listener, self).__init__(self.on_press, self.on_release)
#         self.recorder = recorder

#     def on_press(self, key):
#         try:
#             if event.name == '1':
#                 self.recorder.start_recording()
#         except AttributeError:
#             pass

#     def on_release(self, key):
#         try:
#             if key.char == '1':
#                 self.recorder.stop_recording()
#         except AttributeError:
#             pass

recorder = Recorder()

def on_key_press(event):
    # print(f"key pressed: {event.name}")
    try:
        if event.name == '1':
            recorder.start_recording()
    except AttributeError:
        pass

def on_key_release(event):
    # print(f"key released: {event.name}")
    try:
        if event.name == '1':
            recorder.stop_recording()
    except AttributeError:
        pass

def on_event(event):
    if event.event_type == keyboard.KEY_DOWN:
        on_key_press(event)
    elif event.event_type == keyboard.KEY_UP:
        on_key_release(event)

if __name__ == "__main__":
    try:
        load_dotenv()
        client = Anthropic()
        print("Hold shift to speak to Garth...")
        recorder = Recorder()
        # listener = Listener(recorder)
        # listener.start()
        # listener.join()
        keyboard.hook(on_event)

        # Block forever (until Ctrl+C)
        keyboard.wait()

    except KeyboardInterrupt:
        print(f"\nExiting...")