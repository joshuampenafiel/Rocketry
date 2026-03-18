import subprocess
import datetime

# Generate timestamped filename
filename = datetime.datetime.now().strftime("video_%Y%m%d_%H%M%S.mp4")

cmd = [
    "ffmpeg",
    "-f", "v4l2",              # Use Video4Linux2 (low-level driver)
    "-framerate", "30",        # FPS
    "-video_size", "640x480",  # Resolution
    "-i", "/dev/video0",       # Camera device
    "-vcodec", "libx264",      # Encode to H.264
    "-preset", "veryfast",     # Encoding speed
    "-t", "10",                # Duration (seconds)
    filename
]

print(f"Recording to {filename}...")

subprocess.run(cmd)

print("Done.")
