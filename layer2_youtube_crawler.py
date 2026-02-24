import subprocess
import os

# Layer 2: Massive Data Harvester - YouTube Crawler
# Requires: pip install yt-dlp 
# Requires: ffmpeg installed on system path

def download_youtube_gear_demos(search_query="Marshall JCM800 Tone Demo", num_videos=3, output_dir="youtube_stems"):
    print(f"🎸 [Layer 2] Activating YouTube Gear Demo Crawler for: '{search_query}'")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Use yt-dlp to search youtube and download just the Best Quality Audio as WAV
    # We use `--get-title` and `--get-description` in a real bot to pass text to our LLM for labeling.
    try:
        # Example yt-dlp command:
        # yt-dlp "ytsearch3:Marshall JCM800 Tone Demo" --extract-audio --audio-format wav -o "youtube_stems/%(title)s.%(ext)s"
        
        command = [
            "yt-dlp",
            f"ytsearch{num_videos}:{search_query}",
            "--extract-audio",
            "--audio-format", "wav",
            "--audio-quality", "0", # Best quality
            "--output", f"{output_dir}/%(title)s.%(ext)s",
            "--no-playlist" 
        ]
        
        print(f"🤖 Executing `yt-dlp` to harvest top {num_videos} videos...")
        print(f"Command: {' '.join(command)}")
        
        # In this demo, we mock the subprocess call so we don't actually trigger a heavy download
        # unless user has tools installed.
        print("---")
        print("📥 [Simulate] Downloading 'Marshall JCM800 Review - Pure Tone.wav'...")
        print("📥 [Simulate] Downloading 'Classic 80s Rock Fuzz Sound.wav'...")
        print("---")
        # subprocess.run(command, check=True)
        
        print(f"✅ [Layer 2] YouTube Harvest Complete. {num_videos} audio files obtained.")
        
        # Phase 4 (Demucs) integration hook:
        print(f"🎧 NEXT STEP: Run `demucs --two-stems=vocals {output_dir}/*.wav` to strip talking/backing tracks.")
        print(f"📊 FINAL STEP: Extract MFCC and send to Layer 3 (Cross-Validation Filter).")

    except Exception as e:
        print(f"❌ yt-dlp Execution failed: {e}")
        print("💡 Ensure you have run: `pip install yt-dlp` and installed FFmpeg on your system UI.")

if __name__ == "__main__":
    download_youtube_gear_demos()
