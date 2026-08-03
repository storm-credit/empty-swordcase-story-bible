# CLAUDE.md — Empty Swordcase Story Bible v3.4

## Mission

이 저장소는 《빈 검함으로 천하를 수집한다》의 최종 설계도·설정집·세계관과 원고 제작 시스템이다. 설계 단계는 v3.4에서 종료됐으며 현재 모드는 `DRAFT_MODE`다. 기본 임무는 새 설정을 확장하는 것이 아니라 승인된 정본을 읽고 회차별 원고를 집필·검수하는 것이다.

최종 승인 ID: `AUTHOR-AUTO-V3.4-20260803`

## Authority

- Final Canon Owner: 작가
- Project Manager / Lead Story Architect: Synapse-PM
- Repository Executor: Claude Code
- Data / CI Auditor: Codex/A10
- Continuity Blocker: A07
- Voice Editor: A09/A11
- Space & Combat: A12/A13
- Payoff Editor: A14

## Canon Reading Order

1. `CLAUDE.md`
2. `AGENTS.md`
3. `data/project_manifest_v3_4.json`
4. `docs/57_FINAL_CANON_FREEZE_V3_4.md`
5. `COMPLETE_BLUEPRINT.md`
6. `WORLD_BIBLE_COMPLETE.md`
7. `data/effective_world_v3_4.json`
8. `data/collection_registry_120_v3_4.json`
9. `data/set_registry_024_v3_4.json`
10. `data/beast_registry_018_v3_4.json`
11. `data/supporting_cast_operability_028_v3_4.json`
12. 해당 화의 `production/blueprints/EPISODES_021_200_SCENE_BLUEPRINT_V3_4.json` 항목
13. 해당 화의 payoff·world-cast-cost·action·continuity 자료
14. 직전 화 원고와 검수 보고서

## Canon Freeze Rule

다음은 별도 변경 제안 없이 수정하지 않는다.

- 담운의 현재 인격과 과거 수장으로부터의 독립성
- 신수 비소유·계약 거절·종료·철회권
- 소유권·귀환·책임 주제
- 5 Act 결말
- 중앙 소유선 절단과 여섯 책임 조각 배송
- 기존 200화의 목표·선택·보상·훅·비용
- S-Tier 8개와 A-Tier 20개의 최종 답

변경이 필요하면 이유·영향 회차·복선 영향·연속성 비용·대체안을 먼저 기록한다. 승인 전에는 정본 파일을 직접 고치지 않는다.

## Draft Gate

한 화를 쓰기 전에 반드시 확인한다.

- 회차 목표·반대자 목표·6개 이상 씬비트
- 직전 훅의 첫 10% 행동 회수
- S/A/CH/IT/C 회수 태그
- 정본 거점·노선·세력·조연·구체 대가
- 수집품·세트·신수의 현재 상태와 소유·귀환·철회 조건
- 활성 부상·장비·권리·지식 상태
- 액션 화의 공간·거리·첫 3합·세 번의 역전·기능 손실
- 등장 조연의 음성·사적 목표·거절선
- 장면 전후 가치와 상태 변화

## Draft Output

- 초고는 `manuscript/drafts/NNN_제목.md`에 저장한다.
- 한 번에 한 화만 작성한다.
- 기존 사건·결말·복선 답을 임의로 추가·변경하지 않는다.
- 초고 뒤 `scripts/validate_manuscript_drafts_v3_0.py`를 실행한다.
- `production/reviews/NNN_PROSE_AUDIT_*.md`에 역할별 판정을 기록한다.
- 작가 승인 전 원고는 draft다.
- 막히거나 계획이 달라지면 변경 위치·원인·정본 영향·복구안을 기록한다.

## Style Gate

- 파편 단문의 연속을 금지한다.
- 전투는 거리·발 위치·궤적·재질·기능 손실을 추적 가능하게 쓴다.
- 풍경은 방향·생활·위험·감정·액션 준비 중 최소 두 기능을 수행한다.
- 복선 정답은 설명보다 선택·관계·장비·제도 변화로 회수한다.
- 조연은 담운이 없어도 자기 목표와 거절선을 가진다.
- 신수는 전리품·펫·세트 부품처럼 묘사하지 않는다.
- 특정 작가의 고유 문체를 모사하지 않는다.

## Validation

```bash
python scripts/finalize_canon_v3_4_complete.py
python scripts/validate_final_canon_v3_4_complete.py
python scripts/validate_manuscript_drafts_v3_0.py
```

## Current Status

- Design Blueprint / Setting Bible / World Bible v3.4 — 완료·동결
- 5 Act / 10 Arc / 20 Subact / 200화 기능 지도 — 완료
- EP021~EP200 Production Blueprint — 180화 / 1,080비트 완료
- 8권역 / 48거점 / 20노선 / 18세력 — 완료
- 수집품 120 / 세트 24 / 신수 18 / 조연 28 — 완료
- Semantic Audit — critical error 0 / warning 0
- Existing drafts — 1~2화
- Author-approved manuscript — 0화
- Next episode — 제3화 「첫 번째 수집」
