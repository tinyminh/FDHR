import subprocess
import tkinter as tk
from tkinter import filedialog
import os

# --- File picker ---
root = tk.Tk()
root.withdraw()  # hide main window

file_path = filedialog.askopenfilename(
    title="Select MP4 Video to Upscale",
    filetypes=[("MP4 files", "*.mp4")]
)

if not file_path:
    print("No file selected. Exiting.")
    exit()

# --- Output file ---
base, ext = os.path.splitext(file_path)
output_file = f"{base}_upscaled_4k.mp4"

# --- FFmpeg upscale command ---
# upscale to 3840x2160 (4K), enhance sharpness, HDR-style brightness
# Note: requires ffmpeg installed and in PATH
command = [
    "ffmpeg",
    "-i", file_path,
    "-vf", "scale=3840:2160:flags=lanczos,unsharp=5:5:1.0",
    "-c:v", "libx265",  # HEVC for HDR-like quality
    "-preset", "slow",
    "-crf", "18",        # quality
    "-c:a", "copy",
    output_file
]

print(f"Upscaling {file_path} → {output_file}")
subprocess.run(command)

print("Done!")
