import pyttsx3

engine = pyttsx3.init(driverName='espeak')
voices = engine.getProperty('voices')
# for i, v in enumerate(voices):
#     print(i, v.id)

# Pick a valid voice index from the printed list
engine.setProperty('voice', voices[28].id)
engine.setProperty('volume', 1.0)
engine.say("Hello! Testing text to speech on the Raspberry Pi.")
engine.runAndWait()
