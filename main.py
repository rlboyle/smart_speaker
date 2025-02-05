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

def text_to_speech(text):
    print(text)
    # os.system(f"espeak \"{text}\"")
    # os.system(f"say \"{text}\"") # say works for mac
    # obj = gTTS(text=text, lang='en', slow=False)
    # obj.save("output.mp3")
    # os.system("mpg321 output.mp3") # mpg321 should work for raspberry pi
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[3].id) # change voice
    engine.say(text)
    engine.runAndWait()
    

if __name__ == "__main__":
    try:
        fs = 44100  # Sample rate
        seconds = 4  # Duration of recording
        load_dotenv()
        client = Anthropic()
        while True:
            input("Press Enter to talk to Garth...")
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
            sd.wait()  # Wait until recording is finished
            write('output.wav', fs, myrecording)  # Save as WAV file
            data, fs = sf.read('output.wav', dtype='float32')  
            # sd.play(data, fs)
            # status = sd.wait()  # Wait until file is done playing
            model = whisper.load_model("tiny")
            result = model.transcribe("output.wav", fp16=False)
            # print(result["text"])
            # prompt = input("Say something: ")
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
            # print(message.content[0].text)
    except KeyboardInterrupt:
        print(f"\nExiting...")
    


