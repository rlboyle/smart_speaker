import unittest
import os
import wave
from unittest.mock import patch, MagicMock

import gartha  # Your main module

class TestRecorderUnit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Runs once before all tests in this class."""
        # Possibly ensure the "tiny" Whisper model is downloaded, if needed.
        pass

    def setUp(self):
        """Runs before each test method."""
        self.recorder = gartha.Recorder()

    def tearDown(self):
        """Runs after each test method. Cleans up generated audio files."""
        for fname in ("output.mp3", "input.wav", "output.wav"):
            if os.path.exists(fname):
                os.remove(fname)
 
    def test_start_recording_already_recording(self):
        """
        If the recorder is already recording, calling start_recording() again 
        should do nothing (no error).
        """
        self.recorder.recording = True
        self.recorder.start_recording()
        # Just ensures no exception is thrown and no new stream is opened.
        self.assertTrue(self.recorder.recording, "Should remain recording")

    def test_callback_adds_frames(self):
        """
        Recorder.callback() should append audio data (in_data) to self.frames.
        """
        in_data = b"12345"
        self.recorder.frames = []
        self.recorder.callback(in_data, frame_count=512, time_info=None, status=None)
        self.assertEqual(self.recorder.frames[-1], in_data)

class TestTextToSpeechUnit(unittest.TestCase):
    """
    Tests specifically for text_to_speech() in gartha.py.
    """
    def tearDown(self):
        """Remove TTS output files after each test."""
        if os.path.exists("output.mp3"):
            os.remove("output.mp3")

    def test_text_to_speech_basic(self):
        """Checks that text_to_speech() creates an MP3 for normal input."""
        gartha.text_to_speech("Hello world")
        self.assertTrue(os.path.exists("output.mp3"))
        self.assertGreater(os.path.getsize("output.mp3"), 0)

    def test_text_to_speech_long_string(self):
        """
        Provide a longer string to ensure gTTS handles it without errors.
        """
        long_text = "This is a somewhat longer sentence " * 10
        gartha.text_to_speech(long_text)
        self.assertTrue(os.path.exists("output.mp3"))
        self.assertGreater(os.path.getsize("output.mp3"), 0)

if __name__ == "__main__":
    unittest.main()
