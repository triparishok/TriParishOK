#!/usr/bin/env python3
# Validate rendered SEO metadata for review and live Hugo builds.

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from urllib.parse import urlparse


class PageInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title_parts: list[str] = []
        self.meta: dict[str, list[str]] = {}
        self.refresh_targets: list[str] = []
        self.canonicals: list[str] = []
        self.internal_candidates: list[str] = []
        self.in_json_ld = False
        self.json_ld_parts: list[str] = []
        self.json_ld_blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs_list) -> None:
        attrs = {key.lower(): (value or "") for key, value in attrs_list}
        tag = tag.lower()

        if tag == "title":
            self.in_title = True

        if tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            content = attrs.get("content", "")
            if key:
                self.meta.setdefault(key.lower(), []).append(content.strip())

            if attrs.get("http-equiv", "").lower() == "refresh":
                parts = content.split(";", 1)
                if len(parts) == 2 and parts[0].strip() == "0":
                    directive = parts[1].strip()
                    if directive.lower().startswith("url="):
                        self.refresh_targets.append(directive[4:].strip())

        if tag == "link":
            rel_tokens = {
                token.strip().lower()
                for token in attrs.get("rel", "").split()
                if token.strip()
            }
            if "canonical" in rel_tokens:
                self.canonicals.append(attrs.get("href", "").strip())

        attribute = "href" if tag in {"a", "link"} else "src"
        if tag in {"a", "link", "img", "script", "iframe", "source"}:
            value = attrs.get(attribute, "").strip()
            if value:
                self.internal_candidates.append(value)

        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self.in_json_ld = True
            self.json_ld_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if tag == "title":
            self.in_title = False

        if tag == "script" and self.in_json_ld:
            self.json_ld_blocks.append("".join(self.json_ld_parts).strip())
            self.in_json_ld = False
            self.json_ld_parts = []

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)

        if self.in_json_ld:
            self.json_ld_parts.append(data)

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_parts).split())


def page_url_path(root: Path, page: Path) -> str:
    relative = page.relative_to(root).as_posix()

    if relative == "index.html":
        return "/"

    if relative.endswith("/index.html"):
        return "/" + relative[: -len("index.html")]

    return "/" + relative


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("public_dir", type=Path)
    parser.add_argument("--expected-base", required=True)
    parser.add_argument(
        "--expect-noindex",
        required=True,
        choices=("yes", "no"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.public_dir.resolve()
    expected_base = args.expected_base.rstrip("/") + "/"
    expected_parts = urlparse(expected_base)
    expected_path = expected_parts.path or "/"
    expect_noindex = args.expect_noindex == "yes"

    errors: list[str] = []
    pages_checked = 0
    structured_types: dict[str, set[str]] = {}

    if not root.exists():
        errors.append(f"Build directory does not exist: {root}")
    else:
        html_pages = sorted(root.rglob("*.html"))

        if not html_pages:
            errors.append(f"No HTML pages found under {root}")

        for page in html_pages:
            pages_checked += 1
            path = page_url_path(root, page)
            text = page.read_text(encoding="utf-8", errors="replace")

            if "localhost" in text:
                errors.append(f"{path}: contains localhost")

            inspector = PageInspector()
            inspector.feed(text)

            is_redirect = bool(inspector.refresh_targets)

            for candidate in inspector.internal_candidates:
                if candidate.startswith(("#", "mailto:", "tel:", "data:")):
                    continue

                parsed_candidate = urlparse(candidate)

                if candidate.startswith("/") and not candidate.startswith("//"):
                    if expected_path != "/" and not candidate.startswith(expected_path):
                        errors.append(
                            f"{path}: root-relative URL drops the expected base path: "
                            f"{candidate}"
                        )
                    continue

                if (
                    parsed_candidate.scheme in ("http", "https")
                    and parsed_candidate.netloc == expected_parts.netloc
                    and not candidate.startswith(expected_base)
                ):
                    errors.append(
                        f"{path}: same-site URL is outside expected base: {candidate}"
                    )

            if is_redirect:
                if len(inspector.refresh_targets) != 1:
                    errors.append(
                        f"{path}: expected one redirect target; "
                        f"found {len(inspector.refresh_targets)}"
                    )

                if len(inspector.canonicals) != 1:
                    errors.append(
                        f"{path}: expected one canonical URL; "
                        f"found {len(inspector.canonicals)}"
                    )
                else:
                    canonical = inspector.canonicals[0]

                    if not canonical.startswith(expected_base):
                        errors.append(
                            f"{path}: redirect canonical is outside expected base: "
                            f"{canonical}"
                        )

                    if (
                        inspector.refresh_targets
                        and inspector.refresh_targets[0] != canonical
                    ):
                        errors.append(
                            f"{path}: redirect target does not match canonical"
                        )

                    target_parts = urlparse(canonical)
                    target_path = target_parts.path
                    if expected_path != "/" and target_path.startswith(expected_path):
                        target_path = "/" + target_path[len(expected_path):].lstrip("/")

                    target_file = (
                        root / target_path.lstrip("/") / "index.html"
                        if target_path.endswith("/")
                        else root / target_path.lstrip("/")
                    )

                    if not target_file.exists():
                        errors.append(
                            f"{path}: redirect destination was not rendered: "
                            f"{canonical}"
                        )

                continue

            if not inspector.title:
                errors.append(f"{path}: missing title")

            descriptions = inspector.meta.get("description", [])
            if len(descriptions) != 1 or not descriptions[0]:
                errors.append(
                    f"{path}: expected one non-empty meta description; "
                    f"found {len(descriptions)}"
                )

            if len(inspector.canonicals) != 1:
                errors.append(
                    f"{path}: expected one canonical URL; "
                    f"found {len(inspector.canonicals)}"
                )
                canonical = ""
            else:
                canonical = inspector.canonicals[0]

                if not canonical.startswith(expected_base):
                    errors.append(
                        f"{path}: canonical is outside expected base: {canonical}"
                    )

            required_meta = (
                "og:title",
                "og:description",
                "og:url",
                "og:image",
                "twitter:card",
                "twitter:title",
                "twitter:description",
                "twitter:image",
            )

            for key in required_meta:
                values = inspector.meta.get(key, [])
                if len(values) != 1 or not values[0]:
                    errors.append(
                        f"{path}: expected one non-empty {key}; found {len(values)}"
                    )

            og_urls = inspector.meta.get("og:url", [])
            if canonical and og_urls and og_urls[0] != canonical:
                errors.append(f"{path}: og:url does not match canonical")

            for image_key in ("og:image", "twitter:image"):
                values = inspector.meta.get(image_key, [])
                if values:
                    parsed = urlparse(values[0])
                    if parsed.scheme not in ("http", "https") or not parsed.netloc:
                        errors.append(
                            f"{path}: {image_key} is not absolute: {values[0]}"
                        )

            robots = " ".join(inspector.meta.get("robots", [])).lower()
            has_noindex = "noindex" in robots

            if expect_noindex and not has_noindex:
                errors.append(f"{path}: review build is missing noindex")

            if not expect_noindex and has_noindex:
                errors.append(f"{path}: live build still contains noindex")

            types: set[str] = set()

            for block in inspector.json_ld_blocks:
                if not block:
                    errors.append(f"{path}: empty JSON-LD block")
                    continue

                try:
                    data = json.loads(block)
                except json.JSONDecodeError as exc:
                    errors.append(f"{path}: invalid JSON-LD: {exc}")
                    continue

                items = data if isinstance(data, list) else [data]

                for item in items:
                    if isinstance(item, dict):
                        schema_type = item.get("@type")
                        if isinstance(schema_type, str):
                            types.add(schema_type)
                        elif isinstance(schema_type, list):
                            types.update(
                                value
                                for value in schema_type
                                if isinstance(value, str)
                            )

            structured_types[path] = types

    if root.exists():
        robots_path = root / "robots.txt"

        if not robots_path.exists():
            errors.append("robots.txt was not generated")
        else:
            robots_text = robots_path.read_text(
                encoding="utf-8",
                errors="replace",
            )

            if expect_noindex:
                if "Sitemap:" in robots_text:
                    errors.append(
                        "review robots.txt should not advertise a sitemap"
                    )
            else:
                expected_sitemap = expected_base + "sitemap.xml"

                if "Allow: /" not in robots_text:
                    errors.append("live robots.txt is missing Allow: /")

                if f"Sitemap: {expected_sitemap}" not in robots_text:
                    errors.append(
                        "live robots.txt has the wrong sitemap URL"
                    )

        sitemap_path = root / "sitemap.xml"

        if not sitemap_path.exists():
            errors.append("sitemap.xml was not generated")
        else:
            try:
                tree = ET.parse(sitemap_path)
                locations = [
                    element.text.strip()
                    for element in tree.findall(
                        ".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
                    )
                    if element.text and element.text.strip()
                ]
            except ET.ParseError as exc:
                errors.append(f"Invalid sitemap.xml: {exc}")
                locations = []

            if not locations:
                errors.append("sitemap.xml contains no URLs")

            for location in locations:
                if not location.startswith(expected_base):
                    errors.append(
                        f"sitemap URL is outside expected base: {location}"
                    )

    if "Organization" not in structured_types.get("/", set()):
        errors.append("Homepage is missing Organization structured data")

    parish_paths = (
        "/our-parishes/st-ann/",
        "/our-parishes/olph/",
        "/our-parishes/mother-of-sorrows/",
    )

    for path in parish_paths:
        if path not in structured_types:
            errors.append(f"Expected parish page was not rendered: {path}")
        elif "CatholicChurch" not in structured_types[path]:
            errors.append(
                f"{path}: missing CatholicChurch structured data"
            )

    print()
    print("SEO audit")
    print(f"Pages checked: {pages_checked}")
    print(f"Expected base: {expected_base}")
    print(
        "Indexing mode: "
        + ("review/noindex" if expect_noindex else "live/indexable")
    )
    print(f"Errors: {len(errors)}")

    if errors:
        print()
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: Titles, descriptions, canonicals, and social metadata are present.")
    print("PASS: Indexing mode matches the selected build configuration.")
    print("PASS: robots.txt and sitemap.xml match the selected base URL.")
    print("PASS: Organization and CatholicChurch structured data are valid JSON.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
