# Smart Speaker: Gartha

## Overview
Gartha is a virtual home assistant designed to provide information and assist with information.
The current iteration runs on a Rasberry Pi 5 with an external microphone and speaker.
Gartha uses Anthropic API to generate responses, Google TTS API for text-to-speech interpretation, and OpenAI Whisper to convert user speech-to-text.
We also include two other models with different text-to-speech libraries. Garth uses a local TTS model and our laptop version uses pyttsx3 for TTS synthesis.

## Installation

### Prerequisites

Install the following on your target device:  
(Garth can run natively on a laptop or be deployed on a raspberry pi)
- Git: [https://git-scm.com/](https://git-scm.com/)
- Python 3.11: [https://git-scm.com/](https://git-scm.com/) (untested on other versions)

The [ffmpeg](https://ffmpeg.org/) command line tool is required for speech-to-text processing:
```bash
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```
The Espeak command line tool is required for our laptop version and Garth, our other Raspberry Pi version
```bash
# on Ubuntu or Debian
sudo apt update && sudo apt install espeak

# on Arch Linux
sudo pacman -S espeak

# on MacOS using Homebrew (https://brew.sh/)
brew install espeak

# on Windows using Chocolatey (https://chocolatey.org/)
choco install espeak

# on Windows using Scoop (https://scoop.sh/)
scoop install espeak
```

### Setup
1. ***Clone the Repository***:
```bash
git clone [repository-url]
cd smart_speaker
```

2. ***Activate Virtual Environment (recommended)***:
```bash
# Create and activate virtual environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on Unix/macOS:
source venv/bin/activate
```

### Dependencies
Run the following command:
```bash
# install required packages
pip install Anthropic python-dotenv pyttsx3 pynput pyaudio wave git+https://github.com/openai/whisper.git evdev gtts 
```

### Environment Setup
Generate API key at [https://console.anthropic.com/](https://console.anthropic.com/)
```bash
# create .env file in local directory
touch .env

# write API key to .env
echo "ANTHROPIC_API_KEY=your_API_key_here" >> .env
```

### Run in Your Native Python Version
To run natively on a laptop:
```bash
python laptop.py # runs TTS locally with pyttsx3
```
To deploy on a raspberry pi:
```bash
python gartha.py # runs with Google TTS API
python gartha.py # runs with espeak local TTS library.
```


