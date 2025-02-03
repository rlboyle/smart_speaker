# brew install espeak
from dotenv import load_dotenv
import os
from anthropic import Anthropic
import sys

def text_to_speech(text):
    os.system(f"espeak \"{text}\"")

# message = client.messages.create(
#     model="claude-3-5-sonnet-20241022",
#     max_tokens=1024,
#     system="You are a helpful smart speaker assistant named Garth. You can assist with my questions and are always positive",
#     messages=[
#         {"role": "user", "content": "Who are you?"}
#     ]
# )
# print(message.content[0].text)

if __name__ == "__main__":
    try:
        load_dotenv()
        client = Anthropic()
        while True:
            prompt = input("Say something: ")
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system="You are a helpful smart speaker assistant named Garth. You can assist with my questions and are always positive",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text_to_speech(message.content[0].text)
            # print(message.content[0].text)
    except KeyboardInterrupt:
        print(f"\nExiting...")
    


