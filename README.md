# Podcast Transcriber

Free, accurate, and local podcast transcription using OpenAI's Whisper model.

## Features

- **100% Free** - Runs entirely on your computer, no API costs
- **Accurate** - Uses OpenAI's Whisper speech recognition
- **Offline** - Works without internet after initial model download
- **Batch Processing** - Transcribe ALL your episodes at once automatically

## Folder Structure

```
Transcriber/
├── input/           ← Put your MP3 files here
├── output/          ← Transcriptions appear here
├── transcribe.py    ← Main script
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Install Python (if not already installed)

**Windows:**
Download Python 3.10+ from: https://www.python.org/downloads/
- **Important**: During installation, check "Add Python to PATH"

**macOS:**
```bash
brew install python
```
Or download from: https://www.python.org/downloads/

### 2. Install Dependencies

Open a terminal in this folder and run:

```bash
pip install -r requirements.txt
```

This installs:
- `openai-whisper` - The transcription model
- `torch` - Required for running the AI model

**Note**: First installation may take a few minutes as it downloads PyTorch.

### 3. Install FFmpeg

Whisper needs FFmpeg to process audio files.

**macOS (Recommended):**
```bash
brew install ffmpeg
```

**Windows (Option 1 - Recommended):**
```bash
winget install FFmpeg
```

**Windows (Option 2 - Manual):**
1. Download from: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
2. Extract the zip file
3. Add the `bin` folder to your system PATH, OR
4. Copy `ffmpeg.exe` into this Transcriber folder

**Linux:**
```bash
sudo apt install ffmpeg    # Ubuntu/Debian
sudo dnf install ffmpeg    # Fedora
```

## Usage

### BATCH MODE (Recommended)

1. **Put all your MP3 files** in the `input` folder
2. **Run the script:**
   ```bash
   python transcribe.py
   ```
3. **Find transcriptions** in the `output` folder

That's it! The script will automatically process ALL MP3 files one after another.

### Alternative: Transcribe specific file/folder

```bash
# Specific file
python transcribe.py "Episode 1.mp3"

# All MP3s in a custom folder
python transcribe.py "C:\Podcasts\MyShow"
```

## Output

Transcriptions are saved as `.txt` files in the `output` folder with the same name as the original MP3.

Example:
- `input/Episode_01.mp3` → `output/Episode_01.txt`
- `input/Episode_02.mp3` → `output/Episode_02.txt`
- `input/Episode_03.mp3` → `output/Episode_03.txt`

## Model Options

Edit `transcribe.py` to change the `MODEL_SIZE` variable:

| Model  | Accuracy | Speed    | VRAM Required |
|--------|----------|----------|---------------|
| tiny   | Basic    | Fastest  | ~1 GB         |
| base   | Good     | Fast     | ~1 GB         |
| small  | Better   | Medium   | ~2 GB         |
| medium | Great    | Slower   | ~5 GB         |
| large  | Best     | Slowest  | ~10 GB        |

**Default is `base`** - good balance of speed and accuracy.

For podcasts with clear audio, `base` or `small` usually works great.
For difficult audio (accents, background noise), try `medium` or `large`.

## Troubleshooting

### "ffmpeg not found" error
Make sure FFmpeg is installed and in your PATH (see step 3 above).

### Transcription is slow
- Use a smaller model (tiny or base)
- If you have an NVIDIA GPU, it will automatically use GPU acceleration

### Out of memory error
- Use a smaller model
- Close other applications
- Try `tiny` model for low-RAM systems

## Tips for Best Results

1. **Clear audio** = Better transcription
2. **One speaker at a time** works better than overlapping speech
3. **English works best**, but Whisper supports 99 languages
4. **Longer episodes** just take more time - no quality difference
