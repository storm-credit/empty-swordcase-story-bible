#!/usr/bin/env python3
"""Apply one distinct scene grammar to each generated Subact blueprint.

This post-processor does not alter canonical episode source fields. It adds
engine-specific instructions to the six generated beats so adjacent Subacts do
not read as the same ten-episode experience with different nouns.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BLUEPRINT = ROOT / "production/blueprints/EPISODES_021_200_SCENE_BLUEPRINT_V3_3.json"
GRAMMAR_PATH = ROOT / "data/subact_scene_grammar_v3_3.json"

PHASE_TO_FIELD = {
    "hook_recovery": "opening_pressure",
    "world_pressure": "rhythm_profile",
    "first_attempt": "attempt_mode",
    "evidence_and_counterpressure": "evidence_mode",
    "irreversible_choice": "climax_mode",
    "reward_cost_and_next_hook": "aftermath_mode",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def render(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def apply() -> dict[str, Any]:
    payload = load(DEFAULT_BLUEPRINT)
    grammar_payload = load(GRAMMAR_PATH)
    grammar_by_id = {record["subact_id"]: record for record in grammar_payload["subacts"]}

    used_engines: set[str] = set()
    for episode in payload["episodes"]:
        subact_id = episode["subact_id"]
        grammar = grammar_by_id[subact_id]
        used_engines.add(grammar["engine"])
        episode["scene_grammar"] = {
            "engine": grammar["engine"],
            "rhythm_profile": grammar["rhythm_profile"],
            "reversal_mode": grammar["reversal_mode"],
            "forbidden_pattern": grammar["forbidden_pattern"],
        }
        for beat in episode["scene_beats"]:
            phase = beat["phase"]
            field = PHASE_TO_FIELD[phase]
            beat["engine_instruction"] = grammar[field]
            if phase == "evidence_and_counterpressure":
                beat["reversal_instruction"] = grammar["reversal_mode"]
            if phase == "irreversible_choice":
                beat["forbidden_pattern"] = grammar["forbidden_pattern"]

    payload["scene_grammar_version"] = "3.3"
    payload["scene_grammar_source"] = "data/subact_scene_grammar_v3_3.json"
    payload["distinct_conflict_engines"] = sorted(used_engines)
    payload["distinct_conflict_engine_count"] = len(used_engines)
    payload["generation_rule"] = (
        "canonical episode fields preserved; six non-destructive beats derived; "
        "one distinct Subact scene grammar applied"
    )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render(apply())

    if args.check:
        actual = DEFAULT_BLUEPRINT.read_text(encoding="utf-8")
        if actual != expected:
            print(f"stale grammar application: {DEFAULT_BLUEPRINT.relative_to(ROOT)}")
            return 1
        print(f"OK: grammar applied to {DEFAULT_BLUEPRINT.relative_to(ROOT)}")
        return 0

    DEFAULT_BLUEPRINT.write_text(expected, encoding="utf-8")
    print(f"updated {DEFAULT_BLUEPRINT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
