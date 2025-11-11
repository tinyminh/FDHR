import subprocess
import tkinter as tk
from tkinter import filedialog
import argparse
import os
import sys

def run_ffmpeg(cmd):
    """Run FFmpeg command and print it"""
    print("Running command:")
    print(" ".join(cmd))
    subprocess.run(cmd)

def upscale_video(input_file, output_file, resolution="3840:2160", video_bitrate="10M",
                  audio_codec="aac", sharpness=5, use_qsv=False, cpu_sharpen=False):
    """
    Upscale video with optional Intel GPU acceleration (QuickSync) and sharpening
    """
    if use_qsv:
        # GPU pass
        base, ext = os.path.splitext(output_file)
        temp_file = f"{base}_qsv_temp.mp4"
        vf_filter = f"scale_qsv={resolution}"
        codec = "hevc_qsv"
        hwaccel = ["-hwaccel", "qsv"]

        cmd = [
            "ffmpeg",
            *hwaccel,
            "-i", input_file,
            "-vf", vf_filter,
            "-c:v", codec,
            "-preset", "slow",
            "-b:v", video_bitrate,
            "-c:a", audio_codec,
            temp_file
        ]
        run_ffmpeg(cmd)

        # Optional CPU pass for sharpening
        if cpu_sharpen and sharpness > 0:
            cmd_sharp = [
                "ffmpeg",
                "-i", temp_file,
                "-vf", f"unsharp={sharpness}:{sharpness}:1.0",
                "-c:v", "libx265",
                "-preset", "slow",
                "-b:v", video_bitrate,
                "-c:a", "copy",
                output_file
            ]
            run_ffmpeg(cmd_sharp)
            os.remove(temp_file)  # cleanup temp GPU file
        else:
            os.rename(temp_file, output_file)  # no sharpening, just rename

    else:
        # CPU-only full filter
        vf_filter = f"scale={resolution}:flags=lanczos"
        if sharpness > 0:
            vf_filter += f",unsharp={sharpness}:{sharpness}:1.0"
        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-vf", vf_filter,
            "-c:v", "libx265",
            "-preset", "slow",
            "-b:v", video_bitrate,
            "-c:a", audio_codec,
            output_file
        ]
        run_ffmpeg(cmd)

def gui_mode():
    """Launch GUI to pick file and run upscale"""
    root = tk.Tk()
    root.withdraw()
    input_file = filedialog.askopenfilename(title="Select MP4 Video", filetypes=[("MP4 files","*.mp4")])
    if not input_file:
        print("No file selected. Exiting.")
        sys.exit(0)

    # Defaults
    resolution = "3840:2160"
    video_bitrate = "10M"
    audio_codec = "aac"
    sharpness = 5
    use_qsv = True
    cpu_sharpen = True

    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_upscaled.mp4"

    upscale_video(input_file, output_file, resolution, video_bitrate, audio_codec, sharpness, use_qsv, cpu_sharpen)
    print("Done! Output:", output_file)

def cli_mode(args):
    if not args.input or not args.output:
        print("CLI mode requires input and output files. Use --gui for GUI mode.")
        sys.exit(1)
    upscale_video(
        args.input,
        args.output,
        args.resolution,
        args.vbitrate,
        args.acodec,
        args.sharpness,
        use_qsv=args.qsv,
        cpu_sharpen=args.cpu_sharpen
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
    parser.add_argument("--cpu-sharpen", action="store_true", help="Apply sharpening in a second CPU pass after QSV upscaling")
    args = parser.parse_args()

    if args.gui:
        gui_mode()
    else:
        cli_mode(args)

if __name__ == "__main__":
    main()
