# Social Media Video Downloader

A small beginner Python project that downloads the video from a public post on X (Twitter), Instagram, Facebook, or Reddit, using the [yt-dlp](https://github.com/yt-dlp/yt-dlp) library to do the heavy lifting. yt-dlp automatically detects which site a link is from, so one script handles all four.

## What it does

You give it a post URL, and it saves the video into a `downloads` folder on your computer.

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
python social_media_downloader.py
```

Or pass the URL directly:

```
python social_media_downloader.py https://x.com/someuser/status/1234567890
```

The video will be saved in a `downloads` folder next to the script.

## A note on Instagram and Facebook

Some posts on these two platforms require you to be logged in to view (private accounts, age-restricted posts, etc.), so those may fail without extra setup. Public posts generally work without any changes needed.

## A note on responsible use

Only download videos you have the right to save — your own posts, or public videos for personal offline viewing. Don't redistribute other people's content without permission; that can run into copyright issues and each platform's terms of service.