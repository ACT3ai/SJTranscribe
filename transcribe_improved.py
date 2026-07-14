"""
Podcast Transcriber - Using OpenAI Whisper (Free & Local)

This script transcribes audio/video files to text using the Whisper model.
It runs completely offline after the initial model download.

BATCH MODE: Yes! Put all your audio/video files in the 'in' folder and run.
            All transcriptions will be saved to the 'out' folder.

Supported Formats: MP3, WAV, MP4, M4A, FLAC, OGG

Usage:
    python transcribe_improved.py                    # Transcribe all files in ./in folder
    python transcribe_improved.py path/to/file.mp3   # Transcribe a specific file
    python transcribe_improved.py path/to/folder     # Transcribe all files in a folder

Models (accuracy vs speed):
    - tiny:   Fastest, least accurate (~1GB VRAM)
    - base:   Fast, decent accuracy (~1GB VRAM) [DEFAULT]
    - small:  Good balance (~2GB VRAM)
    - medium: Very accurate (~5GB VRAM)
    - large:  Most accurate, slowest (~10GB VRAM)
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

try:
    import whisper
except ImportError:
    print("\n❌ OpenAI Whisper is not installed.")
    print("\nInstalling whisper...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai-whisper"])
        import whisper
        print("✅ Whisper installed successfully!")
    except Exception as e:
        print(f"\n❌ Failed to install whisper: {e}")
        print("\nPlease install manually:")
        print("    pip install openai-whisper")
        sys.exit(1)


# Configuration - Change these as needed
MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large

# Folder paths (relative to script location)
SCRIPT_DIR = Path(__file__).parent
INPUT_FOLDER = SCRIPT_DIR / "in"     # Changed from "input" to "in"
OUTPUT_FOLDER = SCRIPT_DIR / "out"   # Changed from "output" to "out"

# Supported audio/video extensions
SUPPORTED_EXTENSIONS = {'.mp3', '.wav', '.mp4', '.m4a', '.flac', '.ogg'}


def ensure_folders_exist():
    """Create in/out folders if they don't exist."""
    INPUT_FOLDER.mkdir(exist_ok=True)
    OUTPUT_FOLDER.mkdir(exist_ok=True)


def get_audio_files(path: str = None) -> list[str]:
    """Get all supported audio/video files from a path (file or directory)."""
    if path is None:
        # Default: use the input folder
        path = INPUT_FOLDER

    path = Path(path)

    if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
        return [str(path)]
    elif path.is_dir():
        # Find all supported files in directory (case insensitive)
        audio_files = []
        for ext in SUPPORTED_EXTENSIONS:
            audio_files.extend(path.glob(f"*{ext}"))
            audio_files.extend(path.glob(f"*{ext.upper()}"))

        # Remove duplicates and sort by name
        audio_files = list(set(audio_files))
        audio_files.sort(key=lambda x: x.name.lower())
        return [str(f) for f in audio_files]
    else:
        return []


def transcribe_file(model, audio_path: str, output_dir: Path = None) -> str:
    """Transcribe a single audio/video file and save the result."""
    audio_path = Path(audio_path)

    # Default to OUTPUT_FOLDER
    if output_dir is None:
        output_dir = OUTPUT_FOLDER

    output_path = output_dir / f"{audio_path.stem}.txt"

    print(f"\n{'='*60}")
    print(f"📁 Processing: {audio_path.name}")
    print(f"📝 Output: {output_path.name}")
    print(f"{'='*60}")

    # Transcribe
    print("🎯 Starting transcription...")
    result = model.transcribe(str(audio_path), verbose=False)

    # Extract text
    text = result["text"].strip()

    # Save to file with metadata
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Transcription of: {audio_path.name}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Model used: whisper-{MODEL_SIZE}\n")
        f.write("=" * 60 + "\n\n")
        f.write(text)

    print(f"✅ Transcription complete: {output_path.name}")
    print(f"   Word count: ~{len(text.split())} words")

    return str(output_path)


def main():
    print("\n" + "="*60)
    print("  🎙️  AUDIO TRANSCRIPTION TOOL - Using Whisper")
    print("  📂 BATCH MODE: Processes all files automatically")
    print("="*60)

    # Ensure folders exist
    ensure_folders_exist()

    # Determine input path and output directory
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        custom_path = True
    else:
        input_path = None  # Use default INPUT_FOLDER
        custom_path = False

    # Find audio/video files
    audio_files = get_audio_files(input_path)

    if not audio_files:
        source = input_path if input_path else INPUT_FOLDER
        print(f"\n❌ No supported audio/video files found in: {source}")
        print(f"\n   Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}")
        print("\n" + "-"*60)
        print("HOW TO USE:")
        print("-"*60)
        print(f"\n1. Put your audio/video files in the 'in' folder:")
        print(f"   {INPUT_FOLDER}")
        print(f"\n2. Run: python {Path(__file__).name}")
        print(f"\n3. Find transcriptions in the 'out' folder:")
        print(f"   {OUTPUT_FOLDER}")
        print("\nOR specify a file/folder directly:")
        print(f"   python {Path(__file__).name} episode.mp3")
        print(f"   python {Path(__file__).name} ~/Videos/")
        sys.exit(1)

    print(f"\n📂 Input folder:  {INPUT_FOLDER if not custom_path else input_path}")
    print(f"📂 Output folder: {OUTPUT_FOLDER}")
    print(f"\n📋 Found {len(audio_files)} file(s) to transcribe:")
    for i, f in enumerate(audio_files, 1):
        print(f"   {i}. {Path(f).name}")

    # Load model
    print(f"\n🔧 Loading Whisper '{MODEL_SIZE}' model...")
    print("   (First run will download the model - this may take a few minutes)")

    try:
        model = whisper.load_model(MODEL_SIZE)
        print(f"✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        sys.exit(1)

    # Transcribe each file (BATCH PROCESSING)
    output_files = []
    failed_files = []
    total = len(audio_files)

    for idx, audio_file in enumerate(audio_files, 1):
        print(f"\n[{idx}/{total}] Processing...")
        try:
            output_path = transcribe_file(model, audio_file, OUTPUT_FOLDER)
            output_files.append(output_path)
        except Exception as e:
            print(f"\n❌ Error transcribing {Path(audio_file).name}: {e}")
            failed_files.append(audio_file)

    # Summary
    print("\n" + "="*60)
    print("  📊 BATCH TRANSCRIPTION COMPLETE!")
    print("="*60)
    print(f"\n✅ Successfully transcribed: {len(output_files)} of {total} files")
    if failed_files:
        print(f"❌ Failed: {len(failed_files)}")
    print(f"\n📂 Output folder: {OUTPUT_FOLDER}")
    print("\n📄 Generated files:")
    for f in output_files:
        print(f"   ✓ {Path(f).name}")

    if failed_files:
        print("\n❌ Failed files:")
        for f in failed_files:
            print(f"   ✗ {Path(f).name}")


if __name__ == "__main__":
    main()
