#!/usr/bin/env python3
"""Validate the Pacheon reboot v1 design package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pacheon_reboot_manifest_v1.json"

REQUIRED_FILES = [
    "reboot_v1/00_ORCHESTRA_VERDICT.md",
    "reboot_v1/01_FINAL_PREMISE.md",
    "reboot_v1/02_WORLD_BIBLE.md",
    "reboot_v1/03_POWER_SYSTEM.md",
    "reboot_v1/04_CAST_AND_FACTIONS.md",
    "reboot_v1/05_REGIONS_RELICS_AND_EXPLORATION.md",
    "reboot_v1/06_5ACT_10ARC_20SUBACT.md",
    "reboot_v1/07_FORESHADOWING_AND_PAYOFF.md",
    "reboot_v1/08_MARKET_AND_SERIALIZATION_PACKAGE.md",
    "reboot_v1/09_CANON_FREEZE_V1.md",
    "reboot_v1/episodes/EP001_050_BLUEPRINT.md",
    "reboot_v1/episodes/EP051_100_BLUEPRINT.md",
    "reboot_v1/episodes/EP101_150_BLUEPRINT.md",
    "reboot_v1/episodes/EP151_200_BLUEPRINT.md",
]

EPISODE_FILES = [ROOT / path for path in REQUIRED_FILES if "/episodes/" in path]
EXPECTED_BLADE_MARKS = {
    "흑염도",
    "빙갑검",
    "공절검",
    "몽단검",
    "풍아검",
    "천근도",
    "뇌명극",
    "해문월도",
    "귀영쌍검",
    "명실검",
    "반생검",
    "무명검",
}


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def main() -> int:
    if not MANIFEST.exists():
        fail(f"missing manifest: {MANIFEST.relative_to(ROOT)}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.exists():
            fail(f"missing required file: {relative}")
        if path.stat().st_size < 200:
            fail(f"required file is unexpectedly small: {relative}")

    structure = manifest.get("structure", {})
    expected_structure = {"acts": 5, "arcs": 10, "subacts": 20, "episodes": 200}
    for key, value in expected_structure.items():
        if structure.get(key) != value:
            fail(f"structure.{key} must be {value}, got {structure.get(key)!r}")

    marks = manifest.get("main_blade_marks", [])
    names = {item.get("name") for item in marks}
    if len(marks) != 12:
        fail(f"expected 12 main blade marks, got {len(marks)}")
    if names != EXPECTED_BLADE_MARKS:
        missing = EXPECTED_BLADE_MARKS - names
        extra = names - EXPECTED_BLADE_MARKS
        fail(f"blade mark mismatch; missing={sorted(missing)}, extra={sorted(extra)}")

    episode_numbers: list[int] = []
    title_pattern = re.compile(r"^- EP(\d{3}) 「(.+?)」 — ")
    titles: list[str] = []
    for path in EPISODE_FILES:
        for line in path.read_text(encoding="utf-8").splitlines():
            match = title_pattern.match(line)
            if match:
                episode_numbers.append(int(match.group(1)))
                titles.append(match.group(2).strip())

    expected_numbers = list(range(1, 201))
    if episode_numbers != expected_numbers:
        missing = sorted(set(expected_numbers) - set(episode_numbers))
        duplicates = sorted({n for n in episode_numbers if episode_numbers.count(n) > 1})
        fail(
            "episode sequence mismatch; "
            f"count={len(episode_numbers)}, missing={missing}, duplicates={duplicates}"
        )

    if len(set(titles)) != 200:
        fail("episode titles must be unique across EP001~EP200")

    canon_text = (ROOT / "reboot_v1/09_CANON_FREEZE_V1.md").read_text(encoding="utf-8")
    required_canon_terms = [
        "파천검",
        "파천마검",
        "칼날 없는 자루",
        "REBOOT_MANUSCRIPT_DRAFT_MODE",
        "EP001",
        "EP200",
    ]
    for term in required_canon_terms:
        if term not in canon_text:
            fail(f"canon freeze missing term: {term}")

    if manifest.get("canon", {}).get("deprecated_medium") != "검함":
        fail("manifest must explicitly mark 검함 as deprecated")

    print("[PASS] Pacheon reboot v1 design package")
    print("[PASS] 5 acts / 10 arcs / 20 subacts / 200 episodes")
    print("[PASS] 12 main blade marks")
    print("[PASS] 200 unique episode titles in continuous order")
    return 0


if __name__ == "__main__":
    sys.exit(main())
