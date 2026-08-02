#!/usr/bin/env python3
"""Validate manuscript draft files against the v3.0 prose gate."""
from __future__ import annotations

import re
from pathlib import Path

from lint_prose import lint

ROOT = Path(__file__).resolve().parents[1]
DRAFT_DIR = ROOT / "manuscript" / "drafts"
NAME_RE = re.compile(r"^(\d{3})_.+\.md$")
TITLE_RE = re.compile(r"^#\s*제(\d+)화\s+.+$", re.M)
FORBIDDEN = ["TBD", "TODO", "[CANON GAP]", "[PLACEHOLDER]"]
TAG_RE = re.compile(r"\b(?:S|A|CH|IT|C)\d{2,3}\b")


def body_text(text: str) -> str:
    return re.sub(r"^#.*?\n+", "", text, count=1)


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    match = NAME_RE.match(path.name)
    if not match:
        return [f"invalid filename: {path.name}"]
    episode = int(match.group(1))
    text = path.read_text(encoding="utf-8")
    title = TITLE_RE.search(text)
    if not title or int(title.group(1)) != episode:
        errors.append(f"{path.name}: heading episode mismatch")

    body = body_text(text)
    char_count = len(body)
    if not 4800 <= char_count <= 5800:
        errors.append(f"{path.name}: character count {char_count}, expected 4800-5800")
    for token in FORBIDDEN:
        if token in text:
            errors.append(f"{path.name}: forbidden placeholder {token}")
    if TAG_RE.search(body):
        errors.append(f"{path.name}: internal payoff tag leaked into prose")
    if "첫 번째 미배송품을 찾았습니다" in body:
        errors.append(f"{path.name}: banned system-message hook")
    if lint(path) != 0:
        errors.append(f"{path.name}: prose lint warnings")
    return errors


def main() -> int:
    files = sorted(DRAFT_DIR.glob("*.md"))
    if not files:
        print("no manuscript drafts found")
        return 1
    numbers = [int(NAME_RE.match(path.name).group(1)) for path in files if NAME_RE.match(path.name)]
    if numbers != list(range(1, max(numbers) + 1)):
        print(f"draft coverage is not contiguous: {numbers}")
        return 1

    errors: list[str] = []
    for path in files:
        errors.extend(validate_file(path))
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print(f"MANUSCRIPT DRAFT VALIDATION PASSED: {len(files)} episode(s), 1-{max(numbers)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
