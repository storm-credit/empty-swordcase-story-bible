#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
load=lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
actions=load(ROOT/"data/action_preflight_v2_9.json")
voices=load(ROOT/"data/supporting_cast_voice_028_v2_9.json")
continuity=load(ROOT/"data/critical_continuity_ledger_v2_9.json")
errors=[]
if len(actions)!=47: errors.append("action preflight must contain 47 episodes")
for a in actions:
    if set(a["zones"])!=set("ABCDE"): errors.append(f"E{a['episode']}: zones incomplete")
    if len(a["opening_three_exchanges"])!=3 or len(a["reversals"])!=3: errors.append(f"E{a['episode']}: action sequence incomplete")
    if any(token in json.dumps(a,ensure_ascii=False) for token in ("TBD","확정 필요","기입]","[A13")): errors.append(f"E{a['episode']}: placeholder remains")
    if len(set(a["distances_paces"].values()))<3: errors.append(f"E{a['episode']}: distances too uniform")
if len(voices)!=28 or len({v['id'] for v in voices})!=28: errors.append("supporting voices must be 28 unique")
if len({v['sample_line'] for v in voices})!=28: errors.append("voice samples must be unique")
for v in voices:
    for field in ('sentence_rhythm','lexicon','reasoning_habit','stress_marker','address_rule','sample_line'):
        if not v.get(field): errors.append(f"{v['id']}: missing {field}")
for c in continuity:
    if not (1<=c['start_episode']<=c['end_episode']<=200): errors.append(f"{c['id']}: invalid range")
    if c['end_episode']==200 and not c['permanent']: errors.append(f"{c['id']}: unresolved non-permanent state")
if errors: raise SystemExit("\n".join(errors))
print("v2.9 prose preflight validation passed")
print(f"actions={len(actions)} voices={len(voices)} continuity_states={len(continuity)}")
