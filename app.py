"""
Social Media Video Downloader — Local Website
-----------------------------------------------
A local website (only reachable from your own computer) with a box where
you can paste one or more post links and download them, with live
progress, thumbnail/title previews, a quality picker, friendlier error
messages, and a history of everything you've downloaded.

Works with X (Twitter), Instagram, Facebook, and Reddit links, using the
yt-dlp library to do the actual downloading.

Setup:
    pip3 install flask yt-dlp

Usage:
    python3 app.py

Then open this address in your browser:
    http://127.0.0.1:5000

Only download videos you have the right to save (your own posts, or for
personal offline viewing). Respect creators and each platform's terms of
service.
"""

import os
import json
import time
import uuid
import threading
from functools import wraps
from urllib.parse import urlparse

from flask import Flask, request, jsonify, render_template_string, send_from_directory
from yt_dlp import YoutubeDL

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
HISTORY_FILE = "history.json"

# Set the APP_PASSWORD environment variable once this is deployed somewhere
# reachable by more than just you (e.g. shared with friends). Locally, with
# no APP_PASSWORD set, everything works exactly as before with no login.
APP_PASSWORD = os.environ.get("APP_PASSWORD")


def require_password(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not APP_PASSWORD:
            return view(*args, **kwargs)
        auth = request.authorization
        if not auth or auth.password != APP_PASSWORD:
            return (
                "Authentication required.",
                401,
                {"WWW-Authenticate": 'Basic realm="Fetch"'},
            )
        return view(*args, **kwargs)

    return wrapped

# In-memory tracker for active/finished download jobs, keyed by a random ID.
# jobs_lock keeps things safe since downloads run in background threads.
jobs = {}
jobs_lock = threading.Lock()

PLATFORM_NAMES = {
    "x.com": "X (Twitter)",
    "twitter.com": "X (Twitter)",
    "instagram.com": "Instagram",
    "facebook.com": "Facebook",
    "fb.watch": "Facebook",
    "reddit.com": "Reddit",
}


def detect_platform(url: str) -> str:
    """Guess a friendly platform name from the URL's domain."""
    try:
        host = (urlparse(url).hostname or "").replace("www.", "")
        for key, name in PLATFORM_NAMES.items():
            if key in host:
                return name
        return "Unknown site"
    except Exception:
        return "Unknown site"


def friendly_error(error) -> str:
    """Turn a raw yt-dlp error into a plain-English explanation."""
    text = str(error).lower()
    if "login" in text or "private" in text or "rate-limit" in text:
        return "This post may be private or require a login to view — try a different public post."
    if "unsupported url" in text:
        return "This link isn't from a supported site (X, Instagram, Facebook, or Reddit)."
    if "certificate" in text:
        return "There was a connection security issue — please try again."
    if "unable to download" in text or "404" in text or "not found" in text:
        return "Couldn't find that post — double check the link is correct and still exists."
    return "Something went wrong: " + str(error)


def load_history() -> list:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE) as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_history(history: list) -> None:
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[:50], f, indent=2)  # keep the most recent 50


def run_download(job_id: str, url: str, quality: str) -> None:
    """Runs in a background thread so the page doesn't have to wait."""

    def progress_hook(d):
        with jobs_lock:
            if job_id not in jobs:
                return
            if d["status"] == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate")
                downloaded = d.get("downloaded_bytes", 0)
                if total:
                    jobs[job_id]["percent"] = round(downloaded / total * 100)
                jobs[job_id]["status"] = "downloading"
            elif d["status"] == "finished":
                jobs[job_id]["percent"] = 100
                jobs[job_id]["status"] = "processing"

    format_map = {
        "best": "best",
        "small": "worst[ext=mp4]/worst",
    }

    options = {
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(uploader)s - %(title)s.%(ext)s"),
        "format": format_map.get(quality, "best"),
        "progress_hooks": [progress_hook],
        "quiet": True,
        "no_warnings": True,
    }

    try:
        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
        with YoutubeDL(options) as ydl:
            # Fetch title/thumbnail first, so the page can show a preview
            # before the actual video file finishes downloading.
            info = ydl.extract_info(url, download=False)
            with jobs_lock:
                jobs[job_id]["title"] = info.get("title") or "Untitled"
                jobs[job_id]["thumbnail"] = info.get("thumbnail")
                jobs[job_id]["status"] = "downloading"

            ydl.download([url])
            filename = os.path.basename(ydl.prepare_filename(info))

        with jobs_lock:
            jobs[job_id]["status"] = "done"
            jobs[job_id]["percent"] = 100
            jobs[job_id]["filename"] = filename
            snapshot = dict(jobs[job_id])

        history = load_history()
        history.insert(0, {
            "title": snapshot["title"],
            "platform": snapshot["platform"],
            "filename": snapshot["filename"],
            "url": snapshot["url"],
            "downloaded_at": time.strftime("%Y-%m-%d %H:%M"),
        })
        save_history(history)

    except Exception as error:
        with jobs_lock:
            jobs[job_id]["status"] = "error"
            jobs[job_id]["error"] = friendly_error(error)


PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fetch — video downloader</title>
<script>
  // Apply the saved theme before the page paints, so there's no flash of the wrong colour.
  (function () {
    var saved = localStorage.getItem('fetch-theme');
    var theme = saved || (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
    document.documentElement.setAttribute('data-theme', theme);
  })();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,600&display=swap" rel="stylesheet">
<style>
  :root, :root[data-theme="dark"] {
    --bg: #0e0e10;
    --surface: #18181b;
    --surface-raised: #1f1f23;
    --border: #2b2b30;
    --text: #f2f1ee;
    --text-muted: #93939c;
    --accent: #e2a13d;
    --accent-ink: #1a1206;
    --success: #4fd1a5;
    --error: #f2867a;
    --shadow: 0 1px 2px rgba(0,0,0,0.4), 0 8px 24px rgba(0,0,0,0.28);
  }
  :root[data-theme="light"] {
    --bg: #f7f5f1;
    --surface: #ffffff;
    --surface-raised: #ffffff;
    --border: #e6e1d8;
    --text: #201d17;
    --text-muted: #7a756a;
    --accent: #b5741a;
    --accent-ink: #fff7ea;
    --success: #1f9d6f;
    --error: #c1483a;
    --shadow: 0 1px 2px rgba(30,25,10,0.05), 0 8px 24px rgba(30,25,10,0.06);
  }
  * { box-sizing: border-box; }
  body {
    font-family: "Inter", system-ui, sans-serif;
    max-width: 700px;
    margin: 0 auto;
    padding: 48px 24px 80px;
    background: var(--bg);
    color: var(--text);
    transition: background 0.2s ease, color 0.2s ease;
  }
  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 36px;
  }
  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: "Source Serif 4", Georgia, serif;
    font-weight: 600;
    font-size: 21px;
    letter-spacing: -0.02em;
  }
  .brand svg { color: var(--accent); }
  #themeToggle {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    padding: 0;
    border-radius: 999px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text-muted);
  }
  #themeToggle:hover { color: var(--text); }
  :root[data-theme="dark"] #themeToggle .icon-moon { display: none; }
  :root[data-theme="light"] #themeToggle .icon-sun { display: none; }
  h1.tagline {
    font-size: 15px;
    font-weight: 500;
    color: var(--text-muted);
    margin: 0 0 28px;
  }
  h2 {
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
    margin: 44px 0 14px;
  }
  p.hint { color: var(--text-muted); font-size: 13px; line-height: 1.5; }
  #dropZone {
    border: 1.5px dashed var(--border);
    border-radius: 12px;
    padding: 4px;
    transition: border-color 0.15s ease, background 0.15s ease;
  }
  #dropZone.drag-active {
    border-color: var(--accent);
    background: var(--surface);
  }
  textarea {
    display: block;
    width: 100%;
    box-sizing: border-box;
    padding: 14px;
    border-radius: 9px;
    border: none;
    background: var(--surface);
    color: var(--text);
    font-family: inherit;
    font-size: 14px;
    resize: vertical;
    min-height: 76px;
  }
  textarea:focus { outline: 2px solid var(--accent); outline-offset: -2px; }
  textarea::placeholder { color: var(--text-muted); }
  .controls {
    display: flex;
    gap: 8px;
    margin-top: 10px;
  }
  select {
    padding: 10px 12px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    font-family: inherit;
    font-size: 13px;
  }
  button {
    padding: 10px 18px;
    border-radius: 8px;
    border: none;
    background: var(--accent);
    color: var(--accent-ink);
    font-family: inherit;
    font-weight: 600;
    font-size: 13px;
    cursor: pointer;
  }
  button:hover { filter: brightness(1.08); }
  button:active { filter: brightness(0.96); }
  .job-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px;
    margin-top: 10px;
    box-shadow: var(--shadow);
  }
  .job-top { display: flex; gap: 12px; align-items: center; }
  .job-thumb {
    width: 56px;
    height: 56px;
    object-fit: cover;
    border-radius: 7px;
    background: var(--surface-raised);
    flex-shrink: 0;
  }
  .job-info { flex: 1; min-width: 0; }
  .job-title { font-size: 14px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .job-platform { font-size: 12px; color: var(--text-muted); margin-top: 1px; }
  .job-status { font-size: 12px; margin-top: 6px; color: var(--text-muted); }
  .job-status.success { color: var(--success); }
  .job-status.error { color: var(--error); }
  .job-bar { height: 5px; border-radius: 4px; background: var(--surface-raised); margin-top: 12px; overflow: hidden; }
  .job-bar-fill { height: 100%; width: 0%; background: var(--accent); transition: width 0.3s ease; }
  .history-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 44px 0 14px;
  }
  .history-header h2 { margin: 0; }
  .history-item {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 10px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
  }
  .history-item:last-child { border-bottom: none; }
  .history-item .hint { margin: 2px 0 0; }
  .copy-btn, .clear-btn, .download-link {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-muted);
    font-weight: 500;
    font-size: 11px;
    padding: 5px 10px;
    flex-shrink: 0;
    border-radius: 8px;
    cursor: pointer;
  }
  .copy-btn:hover, .clear-btn:hover, .download-link:hover { color: var(--text); filter: none; border-color: var(--text-muted); }
  .clear-btn:hover { color: var(--error); border-color: var(--error); }
  .download-link { text-decoration: none; display: inline-block; }
  .history-actions { display: flex; gap: 6px; flex-shrink: 0; }
  .discover {
    margin-top: 52px;
    padding-top: 28px;
    border-top: 1px solid var(--border);
  }
  .discover h2 { margin-top: 0; }
  .platform-links {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
  }
  .platform-pill {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 999px;
    border: 1px solid var(--border);
    color: var(--text);
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    background: var(--surface);
  }
  .platform-pill:hover { border-color: var(--accent); color: var(--accent); }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"></path><path d="m7 10 5 5 5-5"></path><path d="M5 21h14"></path></svg>
      Fetch
    </div>
    <button id="themeToggle" title="Toggle light/dark">
      <svg class="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path></svg>
      <svg class="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
    </button>
  </header>
  <h1 class="tagline">Paste a link, or a few — from X, Instagram, Facebook, or Reddit.</h1>
  <div id="dropZone">
    <textarea id="urls" placeholder="Paste a link here, or drag one in from your browser…&#10;One per line for more than one."></textarea>
  </div>
  <div class="controls">
    <select id="quality">
      <option value="best">Best quality</option>
      <option value="small">Smaller file size</option>
    </select>
    <button id="startBtn">Download</button>
  </div>
  <div id="jobs"></div>
  <div class="history-header">
    <h2>History</h2>
    <button id="clearHistoryBtn" class="clear-btn" type="button">Clear history</button>
  </div>
  <div id="history">
    {% for item in history %}
    <div class="history-item">
      <div>
        <strong>{{ item.title }}</strong>
        <div class="hint">{{ item.platform }} · {{ item.filename }} · {{ item.downloaded_at }}</div>
      </div>
      <div class="history-actions">
        {% if item.filename %}<a class="download-link" href="/download/{{ item.filename | urlencode }}">Download</a>{% endif %}
        {% if item.url %}<button class="copy-btn" data-url="{{ item.url }}">Copy link</button>{% endif %}
      </div>
    </div>
    {% else %}
    <p class="hint">Nothing downloaded yet.</p>
    {% endfor %}
  </div>
  <div class="discover">
    <h2>Looking for more to download?</h2>
    <p class="hint">Browse a platform for a video you want, copy its link, then come back and paste it above.</p>
    <div class="platform-links">
      <a class="platform-pill" href="https://x.com" target="_blank" rel="noopener noreferrer">X</a>
      <a class="platform-pill" href="https://www.instagram.com" target="_blank" rel="noopener noreferrer">Instagram</a>
      <a class="platform-pill" href="https://www.facebook.com" target="_blank" rel="noopener noreferrer">Facebook</a>
      <a class="platform-pill" href="https://www.reddit.com" target="_blank" rel="noopener noreferrer">Reddit</a>
    </div>
  </div>
<script>
// --- Theme toggle ---
document.getElementById('themeToggle').addEventListener('click', function () {
  var current = document.documentElement.getAttribute('data-theme');
  var next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('fetch-theme', next);
});
// --- Drag and drop a link onto the box ---
var dropZone = document.getElementById('dropZone');
['dragenter', 'dragover'].forEach(function (evt) {
  dropZone.addEventListener(evt, function (e) {
    e.preventDefault();
    dropZone.classList.add('drag-active');
  });
});
['dragleave', 'drop'].forEach(function (evt) {
  dropZone.addEventListener(evt, function (e) {
    e.preventDefault();
    dropZone.classList.remove('drag-active');
  });
});
dropZone.addEventListener('drop', function (e) {
  e.preventDefault();
  var dropped = e.dataTransfer.getData('text/uri-list') || e.dataTransfer.getData('text/plain');
  if (!dropped) return;
  var textarea = document.getElementById('urls');
  textarea.value = textarea.value.trim() ? textarea.value.trim() + '\\n' + dropped.trim() : dropped.trim();
});
// --- A short two-note chime when a download finishes, no audio file needed ---
function playDing() {
  try {
    var ctx = new (window.AudioContext || window.webkitAudioContext)();
    var now = ctx.currentTime;
    [660, 880].forEach(function (freq, i) {
      var osc = ctx.createOscillator();
      var gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(0.0001, now + i * 0.12);
      gain.gain.exponentialRampToValueAtTime(0.18, now + i * 0.12 + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + i * 0.12 + 0.25);
      osc.connect(gain).connect(ctx.destination);
      osc.start(now + i * 0.12);
      osc.stop(now + i * 0.12 + 0.3);
    });
  } catch (e) { /* audio not available, silently skip */ }
}
// --- Copy link buttons (works for both server-rendered and freshly added history items) ---
document.getElementById('history').addEventListener('click', function (e) {
  if (!e.target.classList.contains('copy-btn')) return;
  var url = e.target.dataset.url;
  navigator.clipboard.writeText(url).then(function () {
    var original = e.target.textContent;
    e.target.textContent = 'Copied!';
    setTimeout(function () { e.target.textContent = original; }, 1400);
  });
});
// --- Download flow ---
async function startDownload() {
  var raw = document.getElementById('urls').value;
  var urls = raw.split('\\n').map(function (s) { return s.trim(); }).filter(Boolean);
  var quality = document.getElementById('quality').value;
  if (urls.length === 0) return;
  var res = await fetch('/start-download', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({urls: urls, quality: quality})
  });
  var data = await res.json();
  data.job_ids.forEach(trackJob);
  document.getElementById('urls').value = '';
}
function trackJob(jobId) {
  var container = document.getElementById('jobs');
  var card = document.createElement('div');
  card.className = 'job-card';
  card.innerHTML = '<div class="job-top">' +
    '<img class="job-thumb" style="display:none;">' +
    '<div class="job-info">' +
      '<div class="job-title">Starting…</div>' +
      '<div class="job-platform"></div>' +
      '<div class="job-status"></div>' +
    '</div>' +
  '</div>' +
  '<div class="job-bar"><div class="job-bar-fill"></div></div>';
  container.prepend(card);
  var interval = setInterval(async function () {
    var res = await fetch('/status/' + jobId);
    var job = await res.json();
    updateCard(card, job);
    if (job.status === 'done' || job.status === 'error') {
      clearInterval(interval);
      if (job.status === 'done') {
        playDing();
        addHistoryItem(job);
      }
    }
  }, 800);
}
function updateCard(card, job) {
  var thumbEl = card.querySelector('.job-thumb');
  var titleEl = card.querySelector('.job-title');
  var platformEl = card.querySelector('.job-platform');
  var statusEl = card.querySelector('.job-status');
  var fillEl = card.querySelector('.job-bar-fill');
  if (job.thumbnail) {
    thumbEl.src = job.thumbnail;
    thumbEl.style.display = 'block';
  }
  titleEl.textContent = job.title || 'Fetching info…';
  platformEl.textContent = job.platform || '';
  fillEl.style.width = (job.percent || 0) + '%';
  if (job.status === 'error') {
    statusEl.textContent = job.error;
    statusEl.className = 'job-status error';
    fillEl.style.background = 'var(--error)';
  } else if (job.status === 'done') {
    statusEl.innerHTML = 'Done — <a class="download-link" href="/download/' + encodeURIComponent(job.filename) + '">Download</a>';
    statusEl.className = 'job-status success';
  } else {
    statusEl.textContent = job.status + '… ' + (job.percent || 0) + '%';
    statusEl.className = 'job-status';
  }
}
function addHistoryItem(job) {
  var list = document.getElementById('history');
  var empty = list.querySelector('p.hint');
  if (empty) empty.remove();

  var item = document.createElement('div');
  item.className = 'history-item';

  var textWrap = document.createElement('div');
  var titleEl = document.createElement('strong');
  titleEl.textContent = job.title || 'Untitled';
  var hintEl = document.createElement('div');
  hintEl.className = 'hint';
  hintEl.textContent = [job.platform, job.filename, 'just now'].filter(Boolean).join(' · ');
  textWrap.appendChild(titleEl);
  textWrap.appendChild(hintEl);

  var actions = document.createElement('div');
  actions.className = 'history-actions';
  if (job.filename) {
    var downloadLink = document.createElement('a');
    downloadLink.className = 'download-link';
    downloadLink.href = '/download/' + encodeURIComponent(job.filename);
    downloadLink.textContent = 'Download';
    actions.appendChild(downloadLink);
  }
  if (job.url) {
    var copyBtn = document.createElement('button');
    copyBtn.className = 'copy-btn';
    copyBtn.type = 'button';
    copyBtn.dataset.url = job.url;
    copyBtn.textContent = 'Copy link';
    actions.appendChild(copyBtn);
  }

  item.appendChild(textWrap);
  item.appendChild(actions);
  list.prepend(item);
}
document.getElementById('startBtn').addEventListener('click', startDownload);
// --- Clear history ---
document.getElementById('clearHistoryBtn').addEventListener('click', async function () {
  if (!confirm('Clear all download history? This cannot be undone.')) return;
  var res = await fetch('/clear-history', { method: 'POST' });
  if (res.ok) {
    document.getElementById('history').innerHTML = '<p class="hint">Nothing downloaded yet.</p>';
  }
});
</script>
</body>
</html>
"""
@app.route("/", methods=["GET"])
@require_password
def home():
    return render_template_string(PAGE, history=load_history())
@app.route("/start-download", methods=["POST"])
@require_password
def start_download():
    data = request.get_json(force=True)
    urls = [u.strip() for u in data.get("urls", []) if u.strip()]
    quality = data.get("quality", "best")
    job_ids = []
    for url in urls:
        job_id = str(uuid.uuid4())
        with jobs_lock:
            jobs[job_id] = {
                "status": "starting",
                "percent": 0,
                "url": url,
                "platform": detect_platform(url),
                "title": None,
                "thumbnail": None,
                "filename": None,
                "error": None,
            }
        thread = threading.Thread(target=run_download, args=(job_id, url, quality), daemon=True)
        thread.start()
        job_ids.append(job_id)
    return jsonify({"job_ids": job_ids})
@app.route("/status/<job_id>", methods=["GET"])
@require_password
def status(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            return jsonify({"error": "unknown job"}), 404
        return jsonify(job)
@app.route("/clear-history", methods=["POST"])
@require_password
def clear_history():
    save_history([])
    return jsonify({"ok": True})
@app.route("/download/<path:filename>", methods=["GET"])
@require_password
def download_file(filename):
    # send_from_directory keeps this safely inside DOWNLOAD_FOLDER even if
    # filename contains "../" or similar — it 404s rather than escaping the folder.
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
