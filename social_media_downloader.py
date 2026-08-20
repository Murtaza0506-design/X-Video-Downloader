"""
Social Media Video Downloader
------------------------------
A tiny beginner-friendly script that downloads a video from a post URL —
works with X (Twitter), Instagram, Facebook, and Reddit links, using the
yt-dlp library to do the actual work (it automatically detects which site
a link is from).

Usage:
    python social_media_downloader.py
    (then paste a post URL when prompted)

  or, in one line:
    python social_media_downloader.py https://x.com/someuser/status/1234567890

Notes:
  - Instagram and Facebook sometimes require you to be logged in to view a
    post (private accounts, age-restricted content, etc.) — public posts
    usually work fine without any extra setup, but if you hit a login
    error, that's why.
  - Only download videos you have the right to save (your own posts, or
    for personal offline viewing). Respect creators and each platform's
    terms of service.
"""

import sys
import os
from yt_dlp import YoutubeDL


def download_video(url: str, output_folder: str = "downloads") -> None:
    """Download the video at `url` into `output_folder`."""
    os.makedirs(output_folder, exist_ok=True)

    options = {
        "outtmpl": os.path.join(output_folder, "%(uploader)s - %(title)s.%(ext)s"),
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
        url = input("Paste the post URL (X, Instagram, Facebook, or Reddit): ").strip()

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