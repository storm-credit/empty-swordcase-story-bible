#!/usr/bin/env python3
"""Split ten-episode compact source files into individual manuscript drafts.

Existing EP001~EP003 full drafts are preserved unless a source explicitly
contains those episodes. All generated prose remains a draft; frozen v3.4
canon is never modified.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "manuscript" / "compact_sources"
DRAFT_DIR = ROOT / "manuscript" / "drafts"
HEADING = re.compile(r"^## EP(\d{3})\s+(.+?)\s*$", re.MULTILINE)


def safe_title(title: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|]", "_", title).strip()
    return value.replace(" ", "_")


def parse_source(path: Path) -> list[tuple[int, str, str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(HEADING.finditer(text))
    rows: list[tuple[int, str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        episode = int(match.group(1))
        title = match.group(2).strip()
        body = text[match.end():end].strip()
        if not body:
            raise ValueError(f"{path}: EP{episode:03d} has empty prose")
        rows.append((episode, title, body))
    return rows


def render(episode: int, title: str, body: str) -> str:
    chars = len(body)
    return (
        f"# 제{episode}화 {title}\n\n"
        "---\n"
        "status: compact-draft\n"
        "canon: v3.4-final-design-bible\n"
        f"episode: {episode}\n"
        f"title: {title}\n"
        "word_count_unit: chars\n"
        f"word_count: {chars}\n"
        "narrator: 담운\n"
        "---\n\n"
        f"{body}\n"
    )


def main() -> int:
    DRAFT_DIR.mkdir(parents=True, exist_ok=True)
    seen: set[int] = set()
    for path in sorted(SOURCE_DIR.glob("*.md")):
        for episode, title, body in parse_source(path):
            if episode in seen:
                raise ValueError(f"duplicate source episode: EP{episode:03d}")
            seen.add(episode)
            target = DRAFT_DIR / f"{episode:03d}_{safe_title(title)}.md"
            for old in DRAFT_DIR.glob(f"{episode:03d}_*.md"):
                if old != target:
                    old.unlink()
            target.write_text(render(episode, title, body), encoding="utf-8")

    print(f"materialized {len(seen)} compact manuscript episodes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
