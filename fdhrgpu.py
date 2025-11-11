import subprocess
import tkinter as tk
from tkinter import filedialog
import argparse
import os
import sys

def upscale_video(input_file, output_file, resolution, video_bitrate, audio_codec, sharpness, use_qsv=False):
    """
    Upscale a video using FFmpeg with optional Intel GPU acceleration (QuickSync).
    """
    if use_qsv:
        hwaccel = ["-hwaccel", "qsv"]
        scale_filter = f"scale_qsv={resolution}"
        codec = "hevc_qsv"
    else:
        hwaccel = []
        scale_filter = f"scale={resolution}:flags=lanczos"
        codec = "libx265"

    unsharp_filter = f",unsharp={sharpness}:{sharpness}:1.0" if sharpness > 0 else ""
    vf_filter = scale_filter + unsharp_filter

    command = [
        "ffmpeg",
        *hwaccel,
        "-i", input_file,
        "-vf", vf_filter,
        "-c:v", codec,
        "-preset", "slow",
        "-b:v", video_bitrate,
        "-c:a", audio_codec,
        output_file
    ]

    print("Running command:")
    print(" ".join(command))
    subprocess.run(command)

def gui_mode():
    """Launch GUI to pick a file and use default settings"""
    root = tk.Tk()
    root.withdraw()
    input_file = filedialog.askopenfilename(title="Select MP4 Video", filetypes=[("MP4 files","*.mp4")])
    if not input_file:
        print("No file selected. Exiting.")
        sys.exit(0)

    resolution = "3840:2160"  # 4K
    video_bitrate = "10M"
    audio_codec = "aac"
    sharpness = 5
    use_qsv = True  # try Intel GPU if available

    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_upscaled.mp4"

    upscale_video(input_file, output_file, resolution, video_bitrate, audio_codec, sharpness, use_qsv)
    print("Done! Output:", output_file)

def cli_mode(args):
    """Run CLI mode"""
    upscale_video(
        args.input,
        args.output,
        args.resolution,
        args.vbitrate,
        args.acodec,
        args.sharpness,
        use_qsv=args.qsv
    )

def main():
    parser = argparse.ArgumentParser(description="Video Upscaler (CLI/GUI) with optional Intel GPU acceleration")
    parser.add_argument("--gui", action="store_true", help="Launch GUI mode (file picker)")
    parser.add_argument("input", nargs="?", help="Input video file (CLI mode)")
    parser.add_argument("output", nargs="?", help="Output video file (CLI mode)")
    parser.add_argument("--resolution", default="3840:2160", help="Target resolution WxH (default 3840x2160)")
    parser.add_argument("--vbitrate", default="10M", help="Video bitrate (default 10M)")
    parser.add_argument("--acodec", default="aac", help="Audio codec (default aac)")
    parser.add_argument("--sharpness", type=int, default=5, help="Unsharp filter amount (0-10)")
    parser.add_argument("--qsv", action="store_true", help="Use Intel QuickSync GPU acceleration")
    args = parser.parse_args()

    if args.gui:
        gui_mode()
    else:
        if not args.input or not args.output:
            print("CLI mode requires input and output files. Use --gui for GUI mode.")
            sys.exit(1)
        cli_mode(args)

if __name__ == "__main__":
    main()
