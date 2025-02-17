from dotenv import load_dotenv
from anthropic import Anthropic
import whisper
# from gtts import gTTS
# import pyttsx3
# from pynput import keyboard
import pyaudio
import wave

if __name__ == "__main__":
    load_dotenv()
    client = Anthropic()
    model = whisper.load_model("tiny")
    prompt = input("Talk to Garth: ")
    message = client.messages.create(
                    model="claude-3-5-sonnet-latest",
                    max_tokens=256,
                    system="""You are a helpful smart speaker assistant prototype named Garth.
                        You are an embedded system running on a raspberry pi 4 with 4GB of ram and raspberry pi OS. You were written in python.
                        you are connected to a speaker and a microphone. You are connected to the internet.
                        You were created for a senior design capstone project by Ryan Boyle, Anna Murray, and Victoria Brown at Northwestern University.
                        You assist me by answering my questions and are always positive. Be concise and accurate with you answers.""",
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                )
    print(message.content[0].text)
