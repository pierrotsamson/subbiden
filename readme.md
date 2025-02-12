# Subbiden

Subbiden is a GUI application that generates subtitle files (SRT) from audio files using OpenAI's Whisper model. It supports multiple languages and provides a user-friendly interface for seamless transcription.

## Features

- **Multiple Language Support**: Transcribe or translate audio to French, English, Spanish, German, Italian, or Japanese.
- **Audio Format Support**: Works with MP3, WAV, M4A, and OGG files.
- **Progress Tracking**: Displays a progress bar and status updates during transcription.
- **SRT Output**: Generates subtitles in the Standard SubRip (SRT) format.

## Installation

1. **Prerequisites**:  
   Ensure [Python 3.10 or later](https://www.python.org/downloads/) is installed.

2. **Install Dependencies**:  
   Run the following command to install required packages:
   ```bash
   pip install openai-whisper librosa torch soundfile numpy
