"""
Social Media Video Downloader — Local Website
-----------------------------------------------
A simple local website (runs only on your own computer) with a text box
where you paste a post URL and click a button to download the video.
Works with X (Twitter), Instagram, Facebook, and Reddit links, using the
yt-dlp library to do the actual downloading.

Setup:
    pip install flask yt-dlp

Usage:
    python3 app.py

Then open this address in your browser:
    http://127.0.0.1:5000

Only download videos you have the right to save (your own posts, or for
personal offline viewing). Respect creators and each platform's terms of
service.
"""

import os
from flask import Flask, request, render_template_string
from yt_dlp import YoutubeDL

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Video Downloader</title>
<style>
  body {
    font-family: system-ui, sans-serif;
    max-width: 600px;
    margin: 80px auto;
    padding: 0 20px;
    background: #111;
    color: #eee;
  }
  h1 { font-size: 22px; }
  form {
    display: flex;
    gap: 8px;
    margin-top: 20px;
  }
  input[type=text] {
    flex: 1;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #444;
    background: #1c1c1c;
    color: #eee;
    font-size: 14px;
  }
  button {
    padding: 10px 18px;
    border-radius: 6px;
    border: none;
    background: #4f7cff;
    color: white;
    font-size: 14px;
    cursor: pointer;
  }
  button:hover { background: #3a63e0; }
  .message {
    margin-top: 20px;
    padding: 12px 14px;
    border-radius: 6px;
    font-size: 14px;
  }
  .success { background: #16321c; color: #8ee29a; }
  .error { background: #3a1616; color: #f29a9a; }
  p.hint { color: #999; font-size: 13px; }
</style>
</head>
<body>
  <h1>🎬 Social Media Video Downloader</h1>
  <p class="hint">Paste a link from X, Instagram, Facebook, or Reddit and click Download.</p>

  <form method="POST" action="/download">
    <input type="text" name="url" placeholder="Paste post URL here..." required>
    <button type="submit">Download</button>
  </form>

  {% if message %}
    <div class="message {{ 'success' if success else 'error' }}">{{ message }}</div>
  {% endif %}
</body>
</html>
"""


def download_video(url: str, output_folder: str = "downloads") -> str:
    """Download the video at `url` into `output_folder`. Returns the saved filename."""
    os.makedirs(output_folder, exist_ok=True)

    options = {
        "outtmpl": os.path.join(output_folder, "%(uploader)s - %(title)s.%(ext)s"),
        "format": "best",
    }

    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return os.path.basename(filename)


@app.route("/", methods=["GET"])
def home():
    return render_template_string(PAGE, message=None, success=False)


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url", "").strip()

    if not url:
        return render_template_string(PAGE, message="Please paste a URL first.", success=False)

    try:
        filename = download_video(url)
        message = f"Downloaded: {filename} (saved in the 'downloads' folder)"
        return render_template_string(PAGE, message=message, success=True)
    except Exception as error:
        message = f"Something went wrong: {error}"
        return render_template_string(PAGE, message=message, success=False)


if __name__ == "__main__":
    app.run(debug=True)