from pynput import keyboard
import pyaudio
import wave
import whisper

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"

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
        print(result["text"])

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

# input("Press Enter to start recording...")
# myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
# sd.wait()  # Wait until recording is finished
# write('output.wav', fs, myrecording)  # Save as WAV file
# data, fs = sf.read('output.wav', dtype='float32')  
# # sd.play(data, fs)
# # status = sd.wait()  # Wait until file is done playing
if __name__ == "__main__":
    print("Press shift to start/stop recording...")
    recorder = Recorder()
    listener = Listener(recorder)
    listener.start()
    listener.join()