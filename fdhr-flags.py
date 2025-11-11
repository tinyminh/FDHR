import subprocess
import tkinter as tk
from tkinter import filedialog
import argparse
import os
import sys

def upscale_video(input_file, output_file, resolution, video_bitrate, audio_codec, sharpness, lanczos=3):
    """
    Upscale a video using ffmpeg with configurable options.
    """
    scale_filter = f"scale={resolution}:flags=lanczos"
    unsharp_filter = f",unsharp={sharpness}:{sharpness}:1.0" if sharpness > 0 else ""
    vf_filter = scale_filter + unsharp_filter

    command = [
        "ffmpeg",
        "-i", input_file,
        "-vf", vf_filter,
        "-c:v", "libx265",
        "-preset", "slow",
        "-b:v", video_bitrate,
        "-c:a", audio_codec,
        output_file
    ]

    print("Running command:")
    print(" ".join(command))
    subprocess.run(command)

def gui_mode():
    """GUI picker for first-run mode"""
    root = tk.Tk()
    root.withdraw()
    input_file = filedialog.askopenfilename(title="Select MP4 Video", filetypes=[("MP4 files","*.mp4")])
    if not input_file:
        print("No file selected.")
        sys.exit(0)

    # Simple defaults
    resolution = "3840:2160"  # 4K
    video_bitrate = "10M"
    audio_codec = "aac"
    sharpness = 5

    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_upscaled.mp4"

    upscale_video(input_file, output_file, resolution, video_bitrate, audio_codec, sharpness)
    print("Done! Output:", output_file)

def cli_mode():
    parser = argparse.ArgumentParser(description="Video Upscaler (4K/QHD) with sharpness and audio config")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("output", help="Output file name")
    parser.add_argument("--resolution", default="3840:2160", help="Target resolution WxH (default 3840x2160)")
    parser.add_argument("--vbitrate", default="10M", help="Video bitrate (default 10M)")
    parser.add_argument("--acodec", default="aac", help="Audio codec (default aac)")
    parser.add_argument("--sharpness", type=int, default=5, help="Unsharp filter amount (0-10)")
    args = parser.parse_args()

    upscale_video(args.input, args.output, args.resolution, args.vbitrate, args.acodec, args.sharpness)

if __name__ == "__main__":
    # If no arguments → GUI first-run
    if len(sys.argv) == 1:
        gui_mode()
    else:
        cli_mode()
