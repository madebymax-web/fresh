# 🎧 WavTranscribe (fresh)

This project automates the transcription of `.wav` audio files using OpenAI's Whisper model and provides a structured way to review and correct those transcripts, with an evolving correction dictionary for domain-specific accuracy.

---

## 🚀 Features

- 🕵️ **Folder Watcher**: Automatically detects when folders with `.wav` files are dropped into a watched directory.
- 🧠 **Whisper Transcription**: Uses OpenAI's Whisper model to transcribe audio files.
- 📝 **Manual Review**: Interactive CLI tool to correct errors in batches, replacing words/phrases and building a custom correction dictionary.
- 🗃️ **Smart Folder Scanning**: Finds `.wav` files in the dropped folder or inside a `Voice` subfolder.
- 🧩 **Modular Scripts**: Each script handles a specific job for clarity, reusability, and performance.

---

## 📁 Folder Structure

fresh/

├── data/

│   ├── raw/ # Folder being watched for incoming audio folders

│   ├── processed/ # Where final transcripts are saved

│   ├── archive/ # (Optional) Used for storing past jobs

│   └── corrections.json # Dictionary of known transcription corrections

└── 

├── scripts/

│   ├── main.py # Entry point — starts the folder watcher

│   ├── watcher.py # Watches for new folders in /data/raw

│   ├── processor.py # Handles transcription of audio files

│   ├── transcriber.py # Loads Whisper and runs the model

│   ├── file_utils.py # Finds .wav files in main or Voice subfolders

│   ├── review.py # CLI interface to review and correct transcripts

│   ├── config.py # Constants used throughout the project

│   ├── requirements.txt # Python dependencies

│   ├── README.md # This file

└──   

---

## 🛠 How It Works

### 1. Watcher

- `main.py` starts the watcher using `watcher.py`.
- Any folder dropped into `data/raw` is detected.
- The `.wav` files inside (or in a `Voice/` subfolder) are passed to the processor.

### 2. Transcription

- `processor.py` sends `.wav` files to `transcriber.py`, which uses Whisper to transcribe them.
- The transcript for each file is saved to a single `.txt` file in `data/processed/`.

### 3. Manual Review

- Run `review.py` to review transcripts in batches of 10.
- Select specific words or phrases to correct.
- Corrections are saved and stored in `corrections.json` for future automation.

---

## 📦 Installation

1. Clone the repo:

git clone https://github.com/madebymax-web/fresh.git
cd fresh

2. Create and activate a virtual environment (optional but recommended):

python -m venv venv
venv\Scripts\activate 

3. Install dependencies:

pip install -r requirements.txt

-Running the Project-

1. Start the Watcher

python scripts/main.py
-This starts watching the data/raw/ folder for incoming .wav folders.-

2. Review & Correct Transcripts

python scripts/review.py
-This will show transcripts in chunks of 10 and let you select words/phrases to correct.-

⚙️ Configuration
Edit config.py to adjust model settings or paths:

MODEL_NAME = "base"  # Or 'small', 'medium', etc.
RAW_BASE = "data/raw"
PROCESSED_BASE = "data/processed"
ARCHIVE_BASE = "data/archive"
CORRECTIONS_FILE = "data/corrections.json"
