"""
X (Twitter) Video Downloader
-----------------------------
A tiny beginner-friendly script that downloads a video from an X/Twitter
post URL, using the yt-dlp library to do the actual work.

Usage:
    python x_video_downloader.py
    (then paste a post URL when prompted)

  or, in one line:
    python x_video_downloader.py https://x.com/someuser/status/1234567890

Only download videos you have the right to save (your own posts, or for
personal offline viewing). Respect creators and X's terms of service.
"""

import sys
import os
from yt_dlp import YoutubeDL


def download_video(url: str, output_folder: str = "downloads") -> None:
    """Download the video at `url` into `output_folder`."""
    os.makedirs(output_folder, exist_ok=True)

    options = {
        # Save files as: downloads/<post author> - <post title>.<ext>
        "outtmpl": os.path.join(output_folder, "%(uploader)s - %(title)s.%(ext)s"),
        # Prefer a single file that already contains both video and audio,
        # so no extra tools (like ffmpeg) are needed to combine them
        "format": "best",
    }

    print(f"Downloading from: {url}")
    with YoutubeDL(options) as ydl:
        ydl.download([url])
    print(f"Done! Check the '{output_folder}' folder.")


def main() -> None:
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Paste the X/Twitter post URL: ").strip()

    if not url:
        print("No URL provided, exiting.")
        return

    try:
        download_video(url)
    except Exception as error:
        print(f"Something went wrong: {error}")
        print("Double-check the URL is a public post that actually contains a video.")


if __name__ == "__main__":
    main()
