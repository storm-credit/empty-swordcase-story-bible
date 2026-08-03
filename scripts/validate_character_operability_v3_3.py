#!/usr/bin/env python3
"""Validate emotional operability for the existing 28 voice-card characters."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def load(path: str) -> Any:
    full = ROOT / path
    if not full.exists():
        ERRORS.append(f"missing file: {path}")
        return {}
    try:
        return json.loads(full.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        ERRORS.append(f"invalid JSON {path}: {exc}")
        return {}


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def main() -> int:
    voice_cards = load("data/character_voice_cards_v2_9.json")
    overlay = load("data/character_emotional_operability_overlay_v3_3.json")
    beasts_payload = load("data/beast_registry_018_v3_3.json")
    governance = load("data/collection_system_governance_v3_3.json")

    voice_names = list(voice_cards.keys()) if isinstance(voice_cards, dict) else []
    records = overlay.get("characters", []) if isinstance(overlay, dict) else []
    require(len(voice_names) == 28, f"voice-card source must contain 28 characters, found {len(voice_names)}")
    require(len(records) == 28, f"emotional overlay must contain 28 characters, found {len(records)}")
    require(overlay.get("author_approval_required") is True, "character overlay must require author approval")
    require([record.get("id") for record in records] == [f"CH{index:03d}" for index in range(1, 29)], "character IDs must be CH001..CH028")
    overlay_names = [record.get("name") for record in records]
    require(overlay_names == voice_names, "character overlay names/order must exactly match voice-card source")
    require(len(set(overlay_names)) == 28, "character names must be unique")

    required_fields = [
        "source_role", "private_goal", "hidden_insecurity", "refusal_line",
        "personal_loss_from_damun_choice", "choice_without_damun",
        "relationship_pressure", "focus_episodes",
    ]
    for record in records:
        label = record.get("id", "unknown character")
        for field in required_fields:
            require(record.get(field) not in (None, "", []), f"{label} missing/empty field: {field}")
        for field in required_fields[:-1]:
            require(len(record.get(field, "")) >= 18, f"{label} field too vague: {field}")
        episodes = record.get("focus_episodes", [])
        require(episodes == sorted(set(episodes)), f"{label} focus_episodes must be sorted and unique")
        require(all(isinstance(episode, int) and 1 <= episode <= 200 for episode in episodes), f"{label} invalid focus episode")
        require("담운" not in record.get("private_goal", "") or record.get("name") == "담운", f"{label} private goal must not depend on Damun")
        require(any(word in record.get("choice_without_damun", "") for word in ("공개", "선택", "열", "넘", "돌", "중단", "파괴", "배포", "복제", "울", "구조", "인계")), f"{label} choice_without_damun lacks a concrete action")

    corrections = governance.get("effective_corrections", {})
    effective_beast_names: list[str] = []
    for beast in beasts_payload.get("beasts", []):
        effective_beast_names.append(corrections.get(beast.get("id"), {}).get("name", beast.get("name")))
    collisions = sorted(set(overlay_names) & set(effective_beast_names))
    require(not collisions, f"human/beast name collision remains after governance corrections: {collisions}")

    result = {
        "version":"3.3",
        "status":"failed" if ERRORS else "passed",
        "errors":ERRORS,
        "verified_characters":len(records),
        "canon_status":"provisional_candidate_pending_author_approval",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if ERRORS else 0


if __name__ == "__main__":
    raise SystemExit(main())
