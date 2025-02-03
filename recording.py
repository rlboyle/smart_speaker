import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write
import whisper

fs = 44100  # Sample rate
seconds = 4  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
write('output.wav', fs, myrecording)  # Save as WAV file
data, fs = sf.read('output.wav', dtype='float32')  
# sd.play(data, fs)
# status = sd.wait()  # Wait until file is done playing
model = whisper.load_model("tiny")
result = model.transcribe("output.wav", fp16=False)
print(result["text"])