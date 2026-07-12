from pathlib import Path
import os
import re
import sys

public = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("public")
prefix = os.environ.get("GITHUB_PAGES_PREFIX", "/TriParishOK").rstrip("/")

exts = {".html", ".xml", ".css", ".js", ".json", ".webmanifest"}

def should_rewrite(url: str) -> bool:
    return (
        url.startswith("/")
        and not url.startswith("//")
        and not url.startswith(prefix + "/")
    )

quoted_attr = re.compile(
    r'(?P<attr>\b(?:href|src|action)=)(?P<quote>["\'])(?P<url>/(?!/)[^"\']*)(?P=quote)'
)

unquoted_attr = re.compile(
    r'(?P<attr>\b(?:href|src|action)=)(?P<url>/(?!/)[^\s>"\']*)'
)

css_url = re.compile(
    r'url\((?P<quote>["\']?)(?P<url>/(?!/)[^)\'"]+)(?P=quote)\)'
)

def rewrite_quoted(match):
    attr = match.group("attr")
    quote = match.group("quote")
    url = match.group("url")
    if should_rewrite(url):
        url = prefix + url
    return f"{attr}{quote}{url}{quote}"

def rewrite_unquoted(match):
    attr = match.group("attr")
    url = match.group("url")
    if should_rewrite(url):
        url = prefix + url
    return f"{attr}{url}"

def rewrite_css(match):
    quote = match.group("quote") or ""
    url = match.group("url")
    if should_rewrite(url):
        url = prefix + url
    return f"url({quote}{url}{quote})"

changed = 0

for path in public.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in exts:
        continue

    text = path.read_text(errors="ignore")
    original = text

    text = quoted_attr.sub(rewrite_quoted, text)
    text = unquoted_attr.sub(rewrite_unquoted, text)
    text = css_url.sub(rewrite_css, text)

    text = text.replace(f"{prefix}{prefix}/", f"{prefix}/")

    if text != original:
        path.write_text(text)
        changed += 1

print(f"Rewrote root-relative paths in {changed} file(s).")
