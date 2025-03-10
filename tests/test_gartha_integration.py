import unittest
import os
import time
import wave
import whisper

from unittest.mock import patch, MagicMock
from evdev import UInput, ecodes

import gartha

class TestGarthaIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """One-time setup. Could ensure hardware is present, etc."""
        cls.recorder = gartha.Recorder()

    def tearDown(self):
        for fname in ("output.mp3", "input.wav", "output.wav"):
            if os.path.exists(fname):
                os.remove(fname)

    def test_stt_with_hello_short_wav(self):
        
        audio_path = os.path.join("tests", "audio_samples", "hello_short.wav")
        self.assertTrue(
            os.path.exists(audio_path),
            "Missing 'hello_short.wav' in tests/audio_samples/!"
        )

        
        model = whisper.load_model('tiny')
        stt_result = model.transcribe(audio_path, fp16=False)

        self.assertIn(
            "Hello world",
            stt_result["text"],
            f"Expected 'Hello world' in transcription"
        )


    def test_stt_with_alligator_wav(self):
        audio_path = os.path.join("tests", "audio_samples", "alligator.wav")
        self.assertTrue(
            os.path.exists(audio_path),
            "Missing 'alligator.wav' in tests/audio_samples/!"
        )

        model = whisper.load_model('tiny')
        stt_result = model.transcribe(audio_path, fp16=False)
        self.assertIn(
            "Alligator",
            stt_result["text"],
            f"Expected 'Alligator' in transcription"
        )

    def test_stt_with_alpacas_wav(self):
        audio_path = os.path.join("tests", "audio_samples", "alpacas.wav")
        self.assertTrue(
            os.path.exists(audio_path),
            "Missing 'alpacas.wav' in tests/audio_samples/!"
        )
        model = whisper.load_model('tiny')
        stt_result = model.transcribe(audio_path, fp16=False)
        self.assertIn(
            "Alpacas",
            stt_result["text"],
            f"Expected 'Alpacas' in transcription"
        )

    def test_stt_with_comp_eng_wav(self):
        audio_path = os.path.join("tests", "audio_samples", "comp_eng.wav")
        self.assertTrue(
            os.path.exists(audio_path),
            "Missing 'comp_eng.wav' in tests/audio_samples/!"
        )
        model = whisper.load_model('tiny')
        stt_result = model.transcribe(audio_path, fp16=False)
        self.assertIn(
            "Computer Engineering",
            stt_result["text"],
            f"Expected 'Computer Engineering' in transcription"
        )

    def test_stt_with_great_lakes_wav(self):
        audio_path = os.path.join("tests", "audio_samples", "great_lakes.wav")
        self.assertTrue(
            os.path.exists(audio_path),
            "Missing 'great_lakes.wav' in tests/audio_samples/!"
        )
        model = whisper.load_model('tiny')
        stt_result = model.transcribe(audio_path, fp16=False)
        self.assertIn(
            "The great lakes are some of the largest freshwater bodies in the world",
            stt_result["text"],
            f"Expected 'The great lakes are some of the largest freshwater bodies in the world' in transcription"
        )

    def test_stt_with_happy_lemon_wav(self):
        audio_path = os.path.join("tests", "audio_samples", "happy_lemon.wav")
        self.assertTrue(
            os.path.exists(audio_path),
            "Missing 'happy_lemon.wav' in tests/audio_samples/!"
        )
        model = whisper.load_model('tiny')
        stt_result = model.transcribe(audio_path, fp16=False)
        self.assertIn(
            "happy lemon",
            stt_result["text"],
            f"Expected 'happy lemon' in transcription"
        )

    def test_stt_with_project_wav(self):
        audio_path = os.path.join("tests", "audio_samples", "project.wav")
        self.assertTrue(
            os.path.exists(audio_path),
            "Missing 'project.wav' in tests/audio_samples/!"
        )
        model = whisper.load_model('tiny')
        stt_result = model.transcribe(audio_path, fp16=False)
        self.assertIn(
            "I would rather not be working on this project right now",
            stt_result["text"],
            f"Expected 'I would rather not be working on this project right now' in transcription"
        )

    def test_stt_with_school_wav(self):
        audio_path = os.path.join("tests", "audio_samples", "school.wav")
        self.assertTrue(
            os.path.exists(audio_path),
            "Missing 'school.wav' in tests/audio_samples/!"
        )
        model = whisper.load_model('tiny')
        stt_result = model.transcribe(audio_path, fp16=False)
        self.assertIn(
            "School",
            stt_result["text"],
            f"Expected 'School' in transcription"
        )

    def test_stt_with_spring_break_wav(self):
        audio_path = os.path.join("tests", "audio_samples", "spring_break.wav")
        self.assertTrue(
            os.path.exists(audio_path),
            "Missing 'spring_break.wav' in tests/audio_samples/!"
        )
        model = whisper.load_model('tiny')
        stt_result = model.transcribe(audio_path, fp16=False)
        self.assertIn(
            "Spring Break to start",
            stt_result["text"],
            f"Expected 'Spring Break to start' in transcription"
        )

    def test_stt_with_student_wav(self):
        audio_path = os.path.join("tests", "audio_samples", "student.wav")
        self.assertTrue(
            os.path.exists(audio_path),
            "Missing 'student.wav' in tests/audio_samples/!"
        )
        model = whisper.load_model('tiny')
        stt_result = model.transcribe(audio_path, fp16=False)
        self.assertIn(
            "student at Northwestern University",
            stt_result["text"],
            f"Expected 'student at Northwestern University' in transcription"
        )


    def test_evdev_button_press_simulation(self):
        """
        Uses UInput to simulate pressing the PTT (KEY_1).
        This tests the on_key callback logic if running in a separate loop.
        
        NOTE: Since gartha.py's main loop is a blocking read_loop, we can't 
        directly call it here. Instead, we demonstrate how you might 
        simulate an event. A real test might spawn the main loop in a thread.
        """
        
        try:
            ui = UInput()
        except PermissionError:
            self.skipTest("Need permission to create UInput. Fix by giving correct privileges.")

        # We'll simulate pressing KEY_1 (down) => start_recording
        event_down = MagicMock()
        event_down.type = ecodes.EV_KEY
        event_down.code = ecodes.KEY_1
        event_down.value = 1  # 1 = key down
        # In evdev, data.keycode = "KEY_1", data.keystate = data.key_down

       
        def on_key_mock(event):
            if event.type == ecodes.EV_KEY:
                if event.code == ecodes.KEY_1:
                    if event.value == 1:  # key down
                        self.recorder.start_recording()
                    elif event.value == 0:  # key up
                        self.recorder.stop_recording()

        # Press down
        on_key_mock(event_down)
        self.assertTrue(self.recorder.recording, "Recorder should be in recording state after KEY_1 down")

        # Now simulate key up => stop recording
        event_up = MagicMock()
        event_up.type = ecodes.EV_KEY
        event_up.code = ecodes.KEY_1
        event_up.value = 0  # 0 = key up

        on_key_mock(event_up)
        self.assertFalse(self.recorder.recording, "Recorder should be stopped after KEY_1 up")
        self.assertTrue(os.path.exists("input.wav"), "Should create input.wav even if empty frames")

if __name__ == "__main__":
    unittest.main()
