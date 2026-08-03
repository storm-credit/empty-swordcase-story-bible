#!/usr/bin/env python3
"""Validate a complete EP001~EP200 compact manuscript draft."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT_DIR = ROOT / "manuscript" / "drafts"
EPISODE_FILES = [
    "data/episodes_001_010.json", "data/episodes_011_020.json",
    "data/episodes_021_030.json", "data/episodes_031_040.json",
    "data/episodes_041_080.json", "data/episodes_081_120.json",
    "data/episodes_121_160.json", "data/episodes_161_200.json",
]
FORBIDDEN = ("TODO", "TBD", "placeholder", "삽입 예정", "보완 예정", "예시 대사", "미정")
ERRORS: list[str] = []


def body_text(raw: str) -> str:
    lines = raw.splitlines()
    if lines and lines[0].startswith("#"):
        lines = lines[1:]
    while lines and not lines[0].strip():
        lines = lines[1:]
    if lines and lines[0].strip() == "---":
        try:
            closing = lines[1:].index("---") + 1
            lines = lines[closing + 1:]
        except ValueError:
            pass
    return "\n".join(lines).strip()


def main() -> int:
    canon: dict[int, dict] = {}
    for path in EPISODE_FILES:
        for row in json.loads((ROOT / path).read_text(encoding="utf-8")):
            canon[row["episode"]] = row

    drafts: dict[int, Path] = {}
    for path in sorted(DRAFT_DIR.glob("[0-9][0-9][0-9]_*.md")):
        episode = int(path.name[:3])
        if episode in drafts:
            ERRORS.append(f"duplicate draft for EP{episode:03d}")
        drafts[episode] = path

    missing = sorted(set(range(1, 201)) - set(drafts))
    extra = sorted(set(drafts) - set(range(1, 201)))
    if missing:
        ERRORS.append(f"missing episodes: {missing}")
    if extra:
        ERRORS.append(f"unexpected episodes: {extra}")

    for episode in range(1, 201):
        path = drafts.get(episode)
        if not path:
            continue
        raw = path.read_text(encoding="utf-8")
        body = body_text(raw)
        title = canon[episode]["title"]
        if f"제{episode}화" not in raw.splitlines()[0]:
            ERRORS.append(f"EP{episode:03d}: heading number mismatch")
        if title not in raw.splitlines()[0]:
            ERRORS.append(f"EP{episode:03d}: canonical title missing from heading")
        if len(body) < 500:
            ERRORS.append(f"EP{episode:03d}: prose too short ({len(body)} chars)")
        if len(body) > 6200:
            ERRORS.append(f"EP{episode:03d}: prose too long ({len(body)} chars)")
        for token in FORBIDDEN:
            if token.lower() in body.lower():
                ERRORS.append(f"EP{episode:03d}: forbidden token {token}")
        if re.search(r"<[^>]+>", body):
            ERRORS.append(f"EP{episode:03d}: internal angle-bracket tag remains")
        hook = canon[episode]["hook"].strip().rstrip(".")
        hook_terms = [term for term in re.split(r"[· ,.'\"()]+", hook) if len(term) >= 2]
        if hook_terms and not any(term in body[-500:] for term in hook_terms):
            ERRORS.append(f"EP{episode:03d}: ending does not visibly recover canonical hook")

    result = {
        "status": "failed" if ERRORS else "passed",
        "episodes": len(drafts),
        "errors": ERRORS,
        "draft_tier": "complete_compact_first_draft",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if ERRORS else 0


if __name__ == "__main__":
    raise SystemExit(main())
