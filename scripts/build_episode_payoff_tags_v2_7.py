#!/usr/bin/env python3
"""Build full v2.7 per-episode payoff tags and human matrix from compact checked-in sources."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
OUT=ROOT/'production'/'continuity'
OUT.mkdir(parents=True,exist_ok=True)

def load_episodes():
    rows=[]
    for name in ['episodes_001_010.json','episodes_011_020.json','episodes_021_030.json','episodes_031_040.json','episodes_041_080.json','episodes_081_120.json','episodes_121_160.json','episodes_161_200.json']:
        rows.extend(json.loads((DATA/name).read_text(encoding='utf-8')))
    rows=sorted(rows,key=lambda x:x['episode'])
    if [x['episode'] for x in rows] != list(range(1,201)):
        raise SystemExit('episode source coverage must be 1-200')
    return {x['episode']:x for x in rows}

def main():
    tracks=json.loads((DATA/'payoff_tracks_v2_7.json').read_text(encoding='utf-8'))
    index=json.loads((DATA/'episode_payoff_index_001_200.json').read_text(encoding='utf-8'))
    episodes=load_episodes()
    if [x['e'] for x in index] != list(range(1,201)):
        raise SystemExit('payoff index coverage must be 1-200')
    tags=[]
    for x in index:
        ep=x['e']; row=episodes[ep]; phase=(ep-1)%10+1; aid=x['a']
        palette=tracks['sensory_palettes'][aid].split('|')
        image=palette[(phase-1)%len(palette)]
        reward=row.get('reward',''); hook=row.get('hook',''); cost=row.get('cost',''); choice=row.get('choice','')
        a=tracks['a_tier'][aid]
        revisit=list(dict.fromkeys([aid,*x['s'],*x['ch'],*x['it']]))[:8]
        tags.append({
          'episode':ep,'title':row['title'],'active_subact_track_id':aid,
          'new_question_id':x['nq'],'revisit_ids':revisit,'s_tier_ids':x['s'],
          'character_track_ids':x['ch'],'item_track_ids':x['it'],
          'minor_payoff_id':'PREMISE' if ep==1 else f'C{ep-1:03d}',
          'opens_c_tier_id':f'C{ep:03d}',
          'c_tier_status':'terminal_image' if ep==200 else 'open_until_next_episode',
          'sensory_seed':f"{image}가 `{reward or hook or row['title']}`의 상태 변화를 먼저 보여주고, 담운이 그 변화 때문에 이동 순서나 손의 사용을 바꾼다.",
          'current_false_answer':f"{a['false_answer']} {tracks['phase_prompts'][str(phase)]}",
          'action_payoff':f"담운 또는 동료가 `{choice}`을 말로 선언하는 데서 멈추지 않고 실제 행동으로 선택하며, 그 즉시 `{cost}`을 지불한다.",
          'residual_change':f"보상 `{reward}`은 기능과 제한을 함께 남기고, `{hook}`이 다음 화에서 해결해야 할 물리적·관계적 상태가 된다.",
          'terminal_truth_if_subact_end':a['truth'] if phase==10 else None,
          'source_hook':hook,'source_cost':cost,'source_reward':reward,
        })
    (DATA/'episode_payoff_tags_001_200.json').write_text(json.dumps(tags,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# 1~200화 복선·맥거핀·회수 태깅 매트릭스 v2.7','',
           '| 화 | 제목 | A축 | S축 | 인물 | 장치 | 회수→개방 | 신규 질문 |',
           '|---:|---|---|---|---|---|---|---|']
    for t in tags:
        lines.append(f"| {t['episode']} | {t['title']} | {t['active_subact_track_id']} | {', '.join(t['s_tier_ids']) or '—'} | {', '.join(t['character_track_ids'])} | {', '.join(t['item_track_ids'])} | {t['minor_payoff_id']} → {t['opens_c_tier_id']} | {t['new_question_id'] or '—'} |")
    (OUT/'EPISODE_PAYOFF_MATRIX_001_200.md').write_text('\n'.join(lines),encoding='utf-8')
    print('BUILT: 200 payoff tags and matrix')
if __name__=='__main__': main()
