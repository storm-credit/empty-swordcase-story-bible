#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRESS = ROOT / "data/reboot_manuscript_progress_v1.json"
BANNED_MAIN_ENGINE_TERMS = ("검함", "표국 배달부", "원래 주인 찾아주기")


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def body_text(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip("\n")
    return text


def main() -> int:
    if not PROGRESS.exists():
        fail(f"missing progress file: {PROGRESS.relative_to(ROOT)}")

    data = json.loads(PROGRESS.read_text(encoding="utf-8"))
    episodes = data.get("episodes", [])
    completed = data.get("completed_drafts")
    next_episode = data.get("next_episode")

    if completed != len(episodes):
        fail(f"completed_drafts={completed}, episode records={len(episodes)}")

    expected_numbers = list(range(1, completed + 1))
    actual_numbers = [item.get("episode") for item in episodes]
    if actual_numbers != expected_numbers:
        fail(f"episode progress is not continuous: {actual_numbers}")

    if next_episode != completed + 1:
        fail(f"next_episode must be {completed + 1}, got {next_episode}")

    seen_titles: set[str] = set()

    for item in episodes:
        number = item["episode"]
        title = item["title"]
        manuscript_path = ROOT / item["manuscript"]
        review_path = ROOT / item["review"]

        if title in seen_titles:
            fail(f"duplicate manuscript title: {title}")
        seen_titles.add(title)

        if not manuscript_path.exists():
            fail(f"missing manuscript: {manuscript_path.relative_to(ROOT)}")
        if not review_path.exists():
            fail(f"missing review: {review_path.relative_to(ROOT)}")

        text = manuscript_path.read_text(encoding="utf-8")
        body = body_text(text)
        body_chars = len(body.replace("\n", ""))

        if not 4500 <= body_chars <= 5500:
            fail(f"EP{number:03d} body length {body_chars} is outside 4500~5500")

        expected_heading = f"# 제{number}화 {title}"
        if expected_heading not in text:
            fail(f"EP{number:03d} missing heading: {expected_heading}")

        if "상태: draft" not in text:
            fail(f"EP{number:03d} must remain draft before author approval")

        if item.get("body_chars_no_newlines") != body_chars:
            fail(
                f"EP{number:03d} recorded length {item.get('body_chars_no_newlines')} "
                f"does not match actual {body_chars}"
            )

        for term in BANNED_MAIN_ENGINE_TERMS:
            if term in body:
                fail(f"EP{number:03d} contains banned legacy term: {term}")

        review = review_path.read_text(encoding="utf-8")
        if f"EP{number:03d}" not in review or "DRAFT_REVIEW_PASS" not in review:
            fail(f"EP{number:03d} review is incomplete")

        if re.search(r"\b(?:TODO|TBD|PLACEHOLDER)\b", text, re.IGNORECASE):
            fail(f"EP{number:03d} contains placeholder token")

        print(f"[PASS] EP{number:03d} {title}: {body_chars} chars")

    print(f"[PASS] reboot manuscript progress: {completed}/200, next EP{next_episode:03d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
