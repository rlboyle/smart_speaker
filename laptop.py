from dotenv import load_dotenv
from anthropic import Anthropic
import whisper
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

        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))

        result = self.model.transcribe("output.wav", fp16=False)
        # print("sent message: m", result["text"], "m")
        if result["text"] != "" and result["text"] != " ":
            self.messages.append({"role": "user", "content": result["text"]})
            try:
                message = client.messages.create(
                        model="claude-3-5-sonnet-latest",
                        max_tokens=256,
                        system="""You are a helpful smart speaker assistant prototype named Garth.
                                You are an embedded system running on a raspberry pi 5. You were written in python. You are connected to a speaker and a microphone. You are connected to the internet.
                                You were created for a senior design capstone project by Ryan Boyle, Anna Murray, and Victoria Brown at Northwestern University.
                                You assist me by answering my questions and are always positive. Keep in mind that the prompts you are given are translated from a real voice using speech to text software so grammar and syntax may not always be correct.
                                If you don't understand something, ask for clarification. Also remember that your answers will also be fed through a text to speech software, so make sure that you
                                answer as if participating in a live spoken conversation as opposed to a text chat. This means no emojis or numbered lists. You cannot give directions.
                                Prioritize accuracy above all else. Keep your responses short and concise. Do not give extra information""",
                        messages=self.messages
                    )
            except Exception as e:
                text_to_speech("Sorry, I am having trouble connecting to Anthropic. Please try again later.")
                print("Hold the PTT key to talk to Garth...")
                return
        
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