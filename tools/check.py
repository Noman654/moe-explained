#!/usr/bin/env python3
"""
Pre-publish checks for the whole book.

Written after a stray semicolon inside an object literal silently killed an entire
chapter's animation — the page still rendered, the figure just sat there dead. A
browser reports that as one line in a console nobody is watching, so it gets its own
check here.

    python3 tools/check.py

Exits non-zero if anything fails, so it can gate a commit.
"""

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAPTERS = sorted((REPO / "posts").glob("*.html"))
STUB = "<!-- generated-stub -->"

fails, warns = [], []


def check_js_syntax():
    """Every inline <script> must parse. node --check is the cheap oracle."""
    if subprocess.run(["node", "--version"], capture_output=True).returncode != 0:
        warns.append("node not found — skipped JS syntax checks")
        return
    for page in CHAPTERS + [REPO / "index.html"]:
        html = page.read_text(encoding="utf-8")
        for i, block in enumerate(re.findall(r"<script>(.*?)</script>", html, re.S)):
            if not block.strip():
                continue
            tmp = REPO / f".check_{page.stem}_{i}.js"
            tmp.write_text(block, encoding="utf-8")
            r = subprocess.run(["node", "--check", str(tmp)], capture_output=True, text=True)
            tmp.unlink()
            if r.returncode != 0:
                msg = [l for l in r.stderr.splitlines() if "SyntaxError" in l]
                fails.append(f"{page.name} script #{i}: {msg[0] if msg else 'parse error'}")


def check_links():
    """Every relative href must resolve to a file that exists."""
    for page in CHAPTERS + [REPO / "index.html"]:
        html = page.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"#][^"]*)"', html):
            if href.startswith(("http://", "https://", "mailto:", "data:", "/")):
                continue  # remote, inline, or site-absolute (resolved by Pages, not the tree)
            target = (page.parent / href.split("#")[0]).resolve()
            if not target.is_file():
                fails.append(f"{page.name}: dead link -> {href}")


def check_assets():
    """Referenced stylesheets and scripts must exist."""
    for page in CHAPTERS + [REPO / "index.html"]:
        html = page.read_text(encoding="utf-8")
        for src in re.findall(r'<script[^>]+src="([^"]+)"', html) + \
                   re.findall(r'<link[^>]+href="([^"]+\.css)"', html):
            if src.startswith(("http://", "https://")):
                continue
            if not (page.parent / src).resolve().is_file():
                fails.append(f"{page.name}: missing asset -> {src}")


def check_chapter_furniture():
    """A real chapter carries the things the book promises on every page."""
    for page in CHAPTERS:
        html = page.read_text(encoding="utf-8")
        if STUB in html:
            continue                                  # stubs are exempt
        for needle, what in [
            ("giscus-mount", "comments mount"),
            ("Found an error?", "corrections link"),
            ("<h3>Sources for this chapter</h3>", "sources list"),
            ('class="takeaway"', "takeaway box"),
            ('class="problem"', "exercise"),
            ("progressrail", "reading progress rail"),
        ]:
            if needle not in html:
                fails.append(f"{page.name}: missing {what}")
        if 'role="img"' in html and 'aria-label' not in html:
            fails.append(f"{page.name}: figure without aria-label")


def check_unsourced_numbers():
    """Soft check: a chapter quoting figures should cite papers alongside them."""
    for page in CHAPTERS:
        html = page.read_text(encoding="utf-8")
        if STUB in html:
            continue
        if "arxiv.org/abs/" not in html:
            fails.append(f"{page.name}: no primary source links at all")
        n = len(re.findall(r"arxiv\.org/abs/", html))
        if n < 3:
            warns.append(f"{page.name}: only {n} arXiv citations")


def main():
    check_js_syntax()
    check_links()
    check_assets()
    check_chapter_furniture()
    check_unsourced_numbers()

    for w in warns:
        print(f"  WARN  {w}")
    for f in fails:
        print(f"  FAIL  {f}")
    print(f"\n{len(CHAPTERS)} chapters checked — "
          f"{len(fails)} failures, {len(warns)} warnings")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
