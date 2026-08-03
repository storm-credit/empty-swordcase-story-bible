#!/usr/bin/env python3
"""Validate a complete EP001~EP200 compact manuscript draft.

This validator checks compact-draft completeness and canon-hook continuity. It
intentionally does not claim publication-length readiness.
"""

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
WARNINGS: list[str] = []
KOREAN_SUFFIXES = (
    "에게서", "으로부터", "이라고", "이라는", "에서는", "에게", "에서", "으로", "까지", "부터",
    "처럼", "보다", "하고", "하며", "한다", "된다", "했다", "됐다", "이다", "였다", "의", "은", "는",
    "이", "가", "을", "를", "에", "와", "과", "로", "도", "만",
)


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


def normalize_words(text: str) -> list[str]:
    cleaned = re.sub(r"[^0-9A-Za-z가-힣]+", " ", text)
    words: list[str] = []
    for word in cleaned.split():
        stem = word
        for suffix in KOREAN_SUFFIXES:
            if len(stem) - len(suffix) >= 2 and stem.endswith(suffix):
                stem = stem[: -len(suffix)]
                break
        if len(stem) >= 2:
            words.append(stem)
    return words


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

    total_chars = 0
    for episode in range(1, 201):
        path = drafts.get(episode)
        if not path:
            continue
        raw = path.read_text(encoding="utf-8")
        body = body_text(raw)
        total_chars += len(body)
        title = canon[episode]["title"]
        if f"제{episode}화" not in raw.splitlines()[0]:
            ERRORS.append(f"EP{episode:03d}: heading number mismatch")
        if title not in raw.splitlines()[0]:
            ERRORS.append(f"EP{episode:03d}: canonical title missing from heading")
        if len(body) < 180:
            ERRORS.append(f"EP{episode:03d}: compact prose too short ({len(body)} chars)")
        if len(body) > 6200:
            ERRORS.append(f"EP{episode:03d}: prose too long ({len(body)} chars)")
        if episode >= 4 and len(body) < 500:
            WARNINGS.append(f"EP{episode:03d}: publication-length expansion target ({len(body)} chars)")
        for token in FORBIDDEN:
            if token.lower() in body.lower():
                ERRORS.append(f"EP{episode:03d}: forbidden token {token}")
        if re.search(r"<[^>]+>", body):
            ERRORS.append(f"EP{episode:03d}: internal angle-bracket tag remains")

        ending = body[-700:]
        hook_words = normalize_words(canon[episode]["hook"])
        ending_words = normalize_words(ending)
        ending_text = " ".join(ending_words)
        anchors = [word for word in hook_words if len(word) >= 3]
        if anchors and not any(anchor in ending_text for anchor in anchors):
            ERRORS.append(f"EP{episode:03d}: ending does not recover a canonical hook anchor")

    result = {
        "status": "failed" if ERRORS else "passed",
        "episodes": len(drafts),
        "total_body_chars": total_chars,
        "errors": ERRORS,
        "warnings": WARNINGS,
        "draft_tier": "complete_compact_first_draft",
        "publication_ready": False,
        "next_gate": "expand EP004-EP200 to publication length and complete human editorial review",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if ERRORS else 0


if __name__ == "__main__":
    raise SystemExit(main())
