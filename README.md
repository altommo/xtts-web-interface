# XTTS Web Interface

A web interface for XTTS (XTension Text-to-Speech) with voice cloning capabilities. This repository provides a user-friendly web interface for interacting with the XTTS v2 text-to-speech engine.

## Features

- Voice cloning from uploaded audio samples
- Text-to-speech conversion using cloned voices
- Support for multiple languages
- Speech history with playback controls
- Simple web interface for easy interaction

## Requirements

- Python 3.9-3.11 (XTTS does not support Python 3.12+)
- XTTS v2 server running
- Flask

## Setup

### 1. Set up XTTS Server

First, you need to set up the XTTS server:

```bash
# Clone the XTTS streaming server
git clone https://github.com/coqui-ai/xtts-streaming-server.git
cd xtts-streaming-server/server

# Create a Python environment with a compatible version
conda create -n xtts-env python=3.11
conda activate xtts-env

# Install required libraries
pip install -r requirements.txt

# Create a file to run the server
echo 'import uvicorn
from main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)' > run_server.py

# Run the XTTS server
python run_server.py
```

### 2. Set up the Web Interface

While the XTTS server is running, open a new terminal and set up the web interface:

```bash
# Clone this repository
git clone https://github.com/altommo/xtts-web-interface.git
cd xtts-web-interface

# Create a Python environment or use the same as the XTTS server
conda activate xtts-env

# Install Flask
pip install flask requests

# Run the web server
python simple_server.py
```

## Usage

1. Access the web interface at http://your-server-ip:5000
2. Upload a WAV format voice sample (5-10 seconds of clear speech)
3. Enter text to convert to speech
4. Select the desired language
5. Click "Generate Speech" to create the audio
6. View and play all generated speech in the history section

## File Structure

- `simple_server.py`: Flask server that handles the web interface and communicates with the XTTS server
- `templates/index.html`: Web interface for interacting with the system

## Credits

This project builds upon the [XTTS streaming server](https://github.com/coqui-ai/xtts-streaming-server) from Coqui AI.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
