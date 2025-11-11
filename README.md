# FDHR
This is a Python Upscaler. Dependencies needs to be FFmpeg in PATH. And Python 3.13 too, also one of the features in the code is getting deprecated soon. Sorry!
Uhh so this is freeware, please compile it to a binary using PyInstaller. Good if you want it to be daily use.
Flags:
the description i pasted code to chatgpt and it made the conclusion too lazy sorry if it is too Ai-ey
--gui	boolean	False	Launches GUI file picker mode instead of CLI. GUI ignores most other arguments; uses defaults.
input	string	N/A	Input video file (required in CLI mode).
output	string	N/A	Output video file (required in CLI mode).
--resolution	string	"3840:2160"	Target output resolution. Format: WIDTH:HEIGHT (e.g., 2560:1440 for QHD).
--vbitrate	string	"10M"	Video bitrate for encoding. Can use M for Mbps, K for kbps (e.g., 8M).
--acodec	string	"aac"	Audio codec. Example: aac, copy (to keep original audio).
--sharpness	int	5	Unsharp filter amount (0–10). Applies sharpening in CPU mode, or optional CPU pass after QSV.
--qsv	boolean	False	Enable Intel QuickSync GPU acceleration (scaling + encoding).
--cpu-sharpen	boolean	False	If QSV is used, applies sharpening in a second CPU pass. Ignored in CPU-only mode.
