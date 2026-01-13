"""
Podcast Transcriber - Using OpenAI Whisper (Free & Local)

This script transcribes MP3 podcast files to text using the Whisper model.
It runs completely offline after the initial model download.

BATCH MODE: Yes! Put all your MP3 files in the 'input' folder and run.
            All transcriptions will be saved to the 'output' folder.

Usage:
    python transcribe.py                    # Transcribe all MP3s in ./input folder
    python transcribe.py path/to/file.mp3   # Transcribe a specific file
    python transcribe.py path/to/folder     # Transcribe all MP3s in a folder

Models (accuracy vs speed):
    - tiny:   Fastest, least accurate (~1GB VRAM)
    - base:   Fast, decent accuracy (~1GB VRAM)
    - small:  Good balance (~2GB VRAM)
    - medium: Very accurate (~5GB VRAM)
    - large:  Most accurate, slowest (~10GB VRAM)
"""

import os
import sys
import glob
from pathlib import Path
from datetime import datetime

import whisper


# Configuration - Change these as needed
MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large

# Folder paths (relative to script location)
SCRIPT_DIR = Path(__file__).parent
INPUT_FOLDER = SCRIPT_DIR / "input"    # Put your MP3 files here
OUTPUT_FOLDER = SCRIPT_DIR / "output"  # Transcriptions saved here


def ensure_folders_exist():
    """Create input/output folders if they don't exist."""
    INPUT_FOLDER.mkdir(exist_ok=True)
    OUTPUT_FOLDER.mkdir(exist_ok=True)


def get_mp3_files(path: str = None) -> list[str]:
    """Get all MP3 files from a path (file or directory)."""
    if path is None:
        # Default: use the input folder
        path = INPUT_FOLDER
    
    path = Path(path)
    
    if path.is_file() and path.suffix.lower() == ".mp3":
        return [str(path)]
    elif path.is_dir():
        # Find all MP3 files in directory (case insensitive)
        mp3_files = list(path.glob("*.mp3")) + list(path.glob("*.MP3"))
        # Sort by name for consistent ordering
        mp3_files.sort(key=lambda x: x.name.lower())
        return [str(f) for f in mp3_files]
    else:
        return []


def transcribe_file(model, audio_path: str, output_dir: Path = None) -> str:
    """Transcribe a single audio file and save the result."""
    audio_path = Path(audio_path)
    
    # Default to OUTPUT_FOLDER
    if output_dir is None:
        output_dir = OUTPUT_FOLDER
    
    output_path = output_dir / f"{audio_path.stem}.txt"
    
    print(f"\n{'='*60}")
    print(f"Transcribing: {audio_path.name}")
    print(f"{'='*60}")
    
    # Transcribe
    result = model.transcribe(str(audio_path), verbose=False)
    
    # Extract text
    text = result["text"].strip()
    
    # Save to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Transcription of: {audio_path.name}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Model used: whisper-{MODEL_SIZE}\n")
        f.write("=" * 60 + "\n\n")
        f.write(text)
    
    print(f"[OK] Saved transcription to: {output_path}")
    print(f"     Word count: ~{len(text.split())} words")
    
    return str(output_path)


def main():
    print("\n" + "="*60)
    print("  PODCAST TRANSCRIBER - Using Whisper (Free & Local)")
    print("  BATCH MODE: Processes all MP3 files automatically")
    print("="*60)
    
    # Ensure folders exist
    ensure_folders_exist()
    
    # Determine input path and output directory
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        # If custom path provided, save output next to input
        custom_path = True
    else:
        input_path = None  # Use default INPUT_FOLDER
        custom_path = False
    
    # Find MP3 files
    mp3_files = get_mp3_files(input_path)
    
    if not mp3_files:
        source = input_path if input_path else INPUT_FOLDER
        print(f"\n[!] No MP3 files found in: {source}")
        print("\n" + "-"*60)
        print("HOW TO USE:")
        print("-"*60)
        print(f"\n1. Put your MP3 files in the 'input' folder:")
        print(f"   {INPUT_FOLDER}")
        print(f"\n2. Run: python transcribe.py")
        print(f"\n3. Find transcriptions in the 'output' folder:")
        print(f"   {OUTPUT_FOLDER}")
        print("\nOR specify a file/folder directly:")
        print("   python transcribe.py episode.mp3")
        print("   python transcribe.py C:\\Podcasts\\MyShow")
        sys.exit(1)
    
    print(f"\n> Input folder:  {INPUT_FOLDER if not custom_path else input_path}")
    print(f"> Output folder: {OUTPUT_FOLDER}")
    print(f"\nFound {len(mp3_files)} MP3 file(s) to transcribe:")
    for i, f in enumerate(mp3_files, 1):
        print(f"   {i}. {Path(f).name}")
    
    # Load model
    print(f"\nLoading Whisper '{MODEL_SIZE}' model...")
    print("(First run will download the model - this may take a few minutes)")
    
    model = whisper.load_model(MODEL_SIZE)
    print(f"[OK] Model loaded successfully!")
    
    # Transcribe each file (BATCH PROCESSING)
    output_files = []
    total = len(mp3_files)
    
    for idx, mp3_file in enumerate(mp3_files, 1):
        print(f"\n[{idx}/{total}] Processing...")
        try:
            # Always output to OUTPUT_FOLDER for consistency
            output_path = transcribe_file(model, mp3_file, OUTPUT_FOLDER)
            output_files.append(output_path)
        except Exception as e:
            print(f"\n[ERROR] Error transcribing {mp3_file}: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("  BATCH TRANSCRIPTION COMPLETE!")
    print("="*60)
    print(f"\n[OK] Successfully transcribed {len(output_files)} of {len(mp3_files)} files")
    print(f"\nOutput folder: {OUTPUT_FOLDER}")
    print("\nGenerated files:")
    for f in output_files:
        print(f"  - {Path(f).name}")


if __name__ == "__main__":
    main()
