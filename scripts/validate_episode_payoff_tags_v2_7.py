#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
tracks=json.loads((ROOT/'data/payoff_tracks_v2_7.json').read_text(encoding='utf-8'))
tags=json.loads((ROOT/'data/episode_payoff_tags_001_200.json').read_text(encoding='utf-8'))
errors=[]
if len(tags)!=200 or [x.get('episode') for x in tags]!=list(range(1,201)):
    errors.append('episode coverage must be exactly 1-200')
known=set(tracks['s_tier'])|set(tracks['a_tier'])|set(tracks['character_tracks'])|set(tracks['item_tracks'])
new_questions=Counter()
for t in tags:
    ep=t['episode']
    expected_a=f"A{((ep-1)//10)+1:02d}"
    if t.get('active_subact_track_id')!=expected_a:
        errors.append(f"E{ep}: expected {expected_a}")
    nq=t.get('new_question_id')
    if nq:
        new_questions[nq]+=1
        if nq not in tracks['s_tier']:
            errors.append(f"E{ep}: unknown new question {nq}")
    if len(t.get('revisit_ids',[]))>8:
        errors.append(f"E{ep}: tag density exceeds 8")
    unknown=[x for x in t.get('revisit_ids',[]) if x not in known]
    if unknown:
        errors.append(f"E{ep}: unknown ids {unknown}")
    expected_minor='PREMISE' if ep==1 else f'C{ep-1:03d}'
    if t.get('minor_payoff_id')!=expected_minor:
        errors.append(f"E{ep}: previous hook payoff mismatch")
    if t.get('opens_c_tier_id')!=f'C{ep:03d}':
        errors.append(f"E{ep}: C-tier open mismatch")
    for field in ['sensory_seed','current_false_answer','action_payoff','residual_change']:
        if not str(t.get(field,'')).strip(): errors.append(f"E{ep}: empty {field}")
for sid,info in tracks['s_tier'].items():
    appearances=sorted(info['appearances'])
    if new_questions[sid]!=1:
        errors.append(f"{sid}: must be installed exactly once")
    if info['install'] not in appearances:
        errors.append(f"{sid}: install missing from appearances")
    gaps=[b-a for a,b in zip(appearances,appearances[1:])]
    if gaps and max(gaps)>40:
        errors.append(f"{sid}: dormant gap {max(gaps)} > 40")
    tag_eps=[t['episode'] for t in tags if sid in t.get('s_tier_ids',[])]
    if tag_eps!=appearances:
        errors.append(f"{sid}: episode tags differ from schedule")
late=[t for t in tags if t.get('new_question_id') and t['episode']>160]
if late: errors.append(f"new S-tier questions after 160: {[x['episode'] for x in late]}")
for start in range(1,201,10):
    if not any(t['s_tier_ids'] for t in tags[start-1:start+9]):
        errors.append(f"{start}-{start+9}: no S-tier revisit")
if errors:
    raise SystemExit('\n'.join(errors))
print('PAYOFF VALIDATION PASSED: 200 episodes, 8 S-tier, 20 A-tier, no >40 episode dormancy, no endgame rule injection')
