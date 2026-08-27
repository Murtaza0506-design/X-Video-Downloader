#!/usr/bin/env python3
"""
Builds the Tariqa newsletter: merges the shared template with the
evergreen content and one issue's data file, and writes a self-contained
HTML file per issue.

Usage:
    python3 build.py                 # builds every issue in content/issues/
    python3 build.py issue-01        # builds just that one issue

To publish a new issue: add content/issues/issue-NN.json (see issue-01.json
for the shape) and run this script. No template/CSS changes needed.
"""
import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
TEMPLATE_DIR = ROOT / "template"
ASSETS = ROOT / "assets"
OUTPUT = ROOT / "output"


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_evergreen() -> dict:
    evergreen = {}
    for path in sorted((CONTENT / "evergreen").glob("*.json")):
        evergreen[path.stem] = load_json(path)
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


def build_issue(issue_path: Path, env: Environment, evergreen: dict,
                 qa_bank: dict, sayings_bank: dict, dyk_bank: dict,
                 history_series: dict) -> Path:
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

    upcoming_history = []
    subject_id = issue.get("history", {}).get("subject_id")
    series = history_series["series"]
    if subject_id:
        names = [entry["name"] for entry in series if entry["id"] != subject_id]
        upcoming_history = names

    css = (TEMPLATE_DIR / "style.css").read_text(encoding="utf-8")
    khatim_svg = (ASSETS / "khatim.svg").read_text(encoding="utf-8")
    corner_svg = (ASSETS / "corner.svg").read_text(encoding="utf-8")

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
        css=css,
        khatim_svg=khatim_svg,
        corner_svg=corner_svg,
    )

    OUTPUT.mkdir(exist_ok=True)
    out_path = OUTPUT / f"{issue_path.stem}.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


def main():
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    evergreen = load_evergreen()
    qa_bank = index_by_id(load_bank("qa_bank"))
    sayings_bank = index_by_id(load_bank("sayings_bank"))
    dyk_bank = index_by_id(load_bank("did_you_know_bank"))
    history_series = load_bank("history_series")

    if len(sys.argv) > 1:
        targets = [CONTENT / "issues" / f"{sys.argv[1]}.json"]
    else:
        targets = sorted((CONTENT / "issues").glob("issue-*.json"))

    for issue_path in targets:
        out_path = build_issue(
            issue_path, env, evergreen, qa_bank, sayings_bank, dyk_bank, history_series
        )
        print(f"Built {issue_path.name} -> {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
