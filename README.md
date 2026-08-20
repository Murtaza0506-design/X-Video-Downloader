# X (Twitter) Video Downloader

A small beginner Python project that downloads the video from a public X/Twitter post, using the [yt-dlp](https://github.com/yt-dlp/yt-dlp) library to do the heavy lifting.

## What it does

You give it a post URL (like `https://x.com/someuser/status/1234567890`), and it saves the video into a `downloads` folder on your computer.

## Requirements

Python 3.8 or newer, and the `yt-dlp` package.

## Setup

Install the one dependency:

```
pip install yt-dlp
```

## Usage

Run the script and paste a URL when asked:

```
python x_video_downloader.py
```

Or pass the URL directly:

```
python x_video_downloader.py https://x.com/someuser/status/1234567890
```

The video will be saved in a `downloads` folder next to the script.

## A note on responsible use

Only download videos you have the right to save — your own posts, or public videos for personal offline viewing. Don't redistribute other people's content without permission; that can run into copyright issues and X's terms of service.