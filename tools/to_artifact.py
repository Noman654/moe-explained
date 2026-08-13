#!/usr/bin/env python3
"""
Turn a post into a self-contained fragment suitable for publishing as an Artifact.

The repo's posts are complete HTML pages that link ../assets/moe.css, which is what
GitHub Pages wants. Artifacts want the opposite: no <html>/<head>/<body> wrapper,
and every byte inlined (a strict CSP blocks external hosts, including same-origin
stylesheets served from another path).

    python3 tools/to_artifact.py posts/01-why-moe.html /tmp/out.html

Idempotent, no dependencies, no network.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def build(src: Path) -> str:
    html = src.read_text(encoding="utf-8")

    # Keep the <title> — Artifact scans the first 8KB for it.
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    title = m.group(1).strip() if m else src.stem

    # Body only.
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.S | re.I)
    if not m:
        sys.exit(f"{src}: no <body> found")
    body = m.group(1)

    # Inline every local stylesheet the page linked, in order.
    css_parts = []
    for href in re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)', html, re.I):
        if href.startswith(("http://", "https://", "//")):
            sys.exit(f"{src}: remote stylesheet {href!r} would be blocked by CSP")
        path = (src.parent / href).resolve()
        if not path.is_file():
            sys.exit(f"{src}: stylesheet not found: {path}")
        css_parts.append(f"/* ---- inlined from {path.relative_to(REPO)} ---- */\n"
                         + path.read_text(encoding="utf-8"))

    # Any <style> block already in <head> comes after the linked sheets, as in the page.
    for block in re.findall(r"<head.*?>(?:.*?)(<style[^>]*>.*?</style>)", html, re.S | re.I):
        css_parts.append(re.sub(r"</?style[^>]*>", "", block, flags=re.I))

    # Inline local <script src="..."> too — an artifact cannot fetch sibling files,
    # so a left-behind src tag silently kills every animation on the page.
    def inline_script(m):
        src = m.group(1)
        if src.startswith(("http://", "https://", "//")):
            sys.exit(f"{src}: remote script would be blocked by CSP")
        path = (src_dir / src).resolve()
        if not path.is_file():
            sys.exit(f"script not found: {path}")
        return ("<script>\n/* ---- inlined from %s ---- */\n%s\n</script>"
                % (path.relative_to(REPO), path.read_text(encoding="utf-8")))

    src_dir = src.parent
    body = re.sub(r'<script[^>]+src=["\']([^"\']+)["\'][^>]*>\s*</script>',
                  inline_script, body, flags=re.I)

    # Same-page anchors survive; cross-post links would 404 inside an artifact.
    body = re.sub(r'href="(?:\.\./)?(?:posts/)?\d\d-[a-z0-9-]+\.html"',
                  'href="#" data-unpublished="1"', body)
    body = re.sub(r'href="(?:\.\./)?index\.html"', 'href="#" data-unpublished="1"', body)

    css = "\n\n".join(css_parts)
    return f"<title>{title}</title>\n<style>\n{css}\n</style>\n{body}\n"


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip())
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    if not src.is_absolute():
        src = REPO / src
    out = build(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(out, encoding="utf-8")
    print(f"{src.name} -> {dst}  ({len(out):,} bytes)")


if __name__ == "__main__":
    main()
