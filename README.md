# Smart Speaker

## Overview
Smart Speaker is a virtual home assistant designed to provide information and assist with information.
The current iteration runs on a laptop but we aim to run it on a Rasberry Pi 4 with an external microphone and speaker.
The project uses Anthropic API to generate responses, Pyttsx3 for audio to text interpretation, and OpenAI Whisper to convert user speech to text.

## Installation

### Prerequisites

Install the following:
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
pip install Anthropic python-dotenv pyttsx3 pynput pyaudio wave git+https://github.com/openai/whisper.git
```

### Environment Setup
Generate API key at [https://console.anthropic.com/](https://console.anthropic.com/)
```bash
# create .env file in local directory
touch .env

# write API key to .env
echo "ANTHROPIC_API_KEY=your_API_key_here" >> .env
```

## Run
```bash
python main.py
```

