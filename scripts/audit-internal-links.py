#!/usr/bin/env python3
"""Validate rendered internal links, assets, path casing, and fragments."""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        for name in ("href", "src"):
            if values.get(name):
                self.links.append((name, values[name] or ""))
        if values.get("style"):
            for url in re.findall(r"url\(\s*['\"]?([^)'\"\s]+)", values["style"] or ""):
                self.links.append(("style", url))


def rendered_target(root: Path, web_path: str) -> Path:
    relative = web_path.lstrip("/")
    candidate = root / relative
    if not relative or web_path.endswith("/"):
        return candidate / "index.html"
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("public", type=Path)
    parser.add_argument("--expected-base", required=True)
    args = parser.parse_args()

    root = args.public.resolve()
    expected = urlsplit(args.expected_base)
    expected_prefix = expected.path.rstrip("/")
    errors: list[str] = []
    pages: dict[Path, LinkParser] = {}

    for page in root.rglob("*.html"):
        parsed = LinkParser()
        parsed.feed(page.read_text(errors="ignore"))
        pages[page.resolve()] = parsed

    for page, parsed in pages.items():
        relative_page = page.relative_to(root)
        page_path = "/" + str(relative_page.parent).replace(".", "").strip("/")
        if page_path != "/":
            page_path += "/"
        page_url = f"{expected.scheme}://{expected.netloc}{expected_prefix}{page_path}"

        for attribute, raw_url in parsed.links:
            if raw_url.startswith(("mailto:", "tel:", "javascript:", "data:")):
                continue
            absolute = urlsplit(urljoin(page_url, raw_url))
            if absolute.netloc != expected.netloc:
                continue
            if not absolute.path.startswith(expected_prefix + "/") and absolute.path != expected_prefix:
                errors.append(f"{relative_page}: {attribute} escapes site base: {raw_url}")
                continue

            local_path = unquote(absolute.path[len(expected_prefix):] or "/")
            if any(character.isupper() for character in local_path):
                errors.append(f"{relative_page}: mixed-case internal path: {raw_url}")

            target = rendered_target(root, local_path)
            if not target.exists():
                errors.append(f"{relative_page}: missing internal target: {raw_url}")
                continue

            if absolute.fragment and target.suffix == ".html":
                target_parser = pages.get(target.resolve())
                if target_parser and absolute.fragment not in target_parser.ids:
                    errors.append(f"{relative_page}: missing fragment #{absolute.fragment}: {raw_url}")

    print("Internal link and path audit")
    print(f"Pages checked: {len(pages)}")
    print(f"Expected base: {args.expected_base}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"- {error}")
    if errors:
        return 1
    print("PASS: Every internal link and asset stays inside the site base.")
    print("PASS: Every internal destination exists, including linked fragments.")
    print("PASS: Rendered internal paths use lowercase characters.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
