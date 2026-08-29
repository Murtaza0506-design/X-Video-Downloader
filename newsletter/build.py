#!/usr/bin/env python3
"""
Builds the Tariqa newsletter: merges the shared template with the
evergreen content and one issue's data file, and writes a self-contained
HTML file per issue.

Usage:
    python3 build.py                          # active theme, every issue
    python3 build.py issue-01                 # active theme, one issue
    python3 build.py issue-01 --theme NAME     # a specific theme
    python3 build.py issue-01 --all-themes     # every theme in template/themes/,
                                                # one output file per theme (for
                                                # comparing design directions)

Theme names are the filenames (minus .css) in template/themes/. The active
theme (used when --theme/--all-themes are omitted) is set by ACTIVE_THEME
below.

To publish a new issue: add content/issues/issue-NN.json (see issue-01.json
for the shape) and run this script. No template/CSS changes needed.
"""
import argparse
import base64
import json
import mimetypes
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
TEMPLATE_DIR = ROOT / "template"
THEMES_DIR = TEMPLATE_DIR / "themes"
ASSETS = ROOT / "assets"
OUTPUT = ROOT / "output"

ACTIVE_THEME = "emerald-manuscript"


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def data_uri(path: Path) -> str:
    """Inline an image/asset as a data URI so each built issue stays one
    self-contained HTML file (no separate image files to keep alongside it)."""
    mime, _ = mimetypes.guess_type(str(path))
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def load_evergreen() -> dict:
    evergreen = {}
    for path in sorted((CONTENT / "evergreen").glob("*.json")):
        evergreen[path.stem] = load_json(path)
    if "locations" in evergreen:
        for place in evergreen["locations"]["places"]:
            place["photo_data"] = data_uri(ROOT / place["photo"])
    return evergreen


def load_bank(name: str):
    return load_json(CONTENT / "banks" / f"{name}.json")


def index_by_id(items: list) -> dict:
    return {item["id"]: item for item in items}


def resolve_ids(ids: list, indexed: dict, bank_name: str) -> list:
    resolved = []
    for item_id in ids:
        if item_id not in indexed:
            raise KeyError(f"'{item_id}' not found in {bank_name} bank")
        resolved.append(indexed[item_id])
    return resolved


def build_issue(issue_path: Path, theme: str, env: Environment, evergreen: dict,
                 qa_bank: dict, sayings_bank: dict, dyk_bank: dict,
                 history_series: dict, suffix: str = "") -> Path:
    issue = load_json(issue_path)
    masthead = evergreen["masthead"]
    footer = evergreen["footer"]

    qa_items = resolve_ids(issue.get("qa_ids", []), qa_bank, "qa_bank")
    saying_items = resolve_ids(issue.get("saying_ids", []), sayings_bank, "sayings_bank")

    did_you_know = None
    if issue.get("did_you_know_id"):
        did_you_know = dyk_bank.get(issue["did_you_know_id"])
        if did_you_know is None:
            raise KeyError(f"'{issue['did_you_know_id']}' not found in did_you_know bank")

    footer_saying = None
    if issue.get("footer_saying_id"):
        footer_saying = sayings_bank.get(issue["footer_saying_id"])
        if footer_saying is None:
            raise KeyError(f"'{issue['footer_saying_id']}' not found in sayings_bank")

    upcoming_history = []
    subject_id = issue.get("history", {}).get("subject_id")
    series = history_series["series"]
    if subject_id:
        names = [entry["name"] for entry in series if entry["id"] != subject_id]
        upcoming_history = names

    theme_css_path = THEMES_DIR / f"{theme}.css"
    if not theme_css_path.exists():
        raise FileNotFoundError(f"No such theme: {theme} (looked for {theme_css_path})")
    css = theme_css_path.read_text(encoding="utf-8")
    khatim_logo = data_uri(ASSETS / "khatim-logo.jpg")
    corner_svg = (ASSETS / "corner.svg").read_text(encoding="utf-8")

    photo_strip = []
    for photo in issue.get("photo_strip", []):
        resolved = dict(photo)
        resolved["src"] = data_uri(ROOT / photo["src"])
        photo_strip.append(resolved)

    template = env.get_template("newsletter.html.jinja")
    html = template.render(
        masthead=masthead,
        footer=footer,
        evergreen=evergreen,
        issue=issue,
        qa_items=qa_items,
        saying_items=saying_items,
        did_you_know=did_you_know,
        upcoming_history=upcoming_history,
        footer_saying=footer_saying,
        photo_strip=photo_strip,
        css=css,
        khatim_logo=khatim_logo,
        corner_svg=corner_svg,
    )

    OUTPUT.mkdir(exist_ok=True)
    out_path = OUTPUT / f"{issue_path.stem}{suffix}.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


def available_themes() -> list:
    return sorted(p.stem for p in THEMES_DIR.glob("*.css"))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("issue", nargs="?", help="issue slug, e.g. issue-01 (default: all issues)")
    parser.add_argument("--theme", help=f"theme to build (default: {ACTIVE_THEME})")
    parser.add_argument("--all-themes", action="store_true", help="build every theme in template/themes/, one file each")
    args = parser.parse_args()

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    evergreen = load_evergreen()
    qa_bank = index_by_id(load_bank("qa_bank"))
    sayings_bank = index_by_id(load_bank("sayings_bank"))
    dyk_bank = index_by_id(load_bank("did_you_know_bank"))
    history_series = load_bank("history_series")

    if args.issue:
        targets = [CONTENT / "issues" / f"{args.issue}.json"]
    else:
        targets = sorted((CONTENT / "issues").glob("issue-*.json"))

    if args.all_themes:
        themes = [(t, f"--{t}") for t in available_themes()]
    else:
        themes = [(args.theme or ACTIVE_THEME, "")]

    for issue_path in targets:
        for theme, suffix in themes:
            out_path = build_issue(
                issue_path, theme, env, evergreen, qa_bank, sayings_bank, dyk_bank,
                history_series, suffix=suffix,
            )
            print(f"Built {issue_path.name} [{theme}] -> {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
