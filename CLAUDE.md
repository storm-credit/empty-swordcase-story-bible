# CLAUDE.md — Empty Swordcase Story Bible v3.4

## Mission

이 저장소는 《빈 검함으로 천하를 수집한다》의 최종 설계도·설정집·세계관과 원고 제작 시스템이다. 설계 단계는 v3.4에서 종료됐고 EP001~EP200 압축 1차 초고도 완결됐다. 현재 모드는 `EXPANSION_EDIT_MODE`다.

기본 임무는 새 사건을 추가하거나 설정을 확장하는 것이 아니라, 승인된 정본과 압축 초고를 읽고 EP004부터 순서대로 플랫폼 연재 분량으로 확장·검수하는 것이다.

최종 설계 승인 ID: `AUTHOR-AUTO-V3.4-20260803`

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
14. 해당 화의 `manuscript/drafts/NNN_제목.md`
15. 직전 화 원고와 검수 보고서

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

## Expansion Gate

한 화를 장편 확장하기 전에 반드시 확인한다.

- 압축 초고의 사건·선택·비용·마지막 훅
- 회차 목표·반대자 목표·6개 이상 씬비트
- 직전 훅의 첫 10% 행동 회수
- S/A/CH/IT/C 회수 태그
- 정본 거점·노선·세력·조연·구체 대가
- 수집품·세트·신수의 현재 상태와 소유·귀환·철회 조건
- 활성 부상·장비·권리·지식 상태
- 액션 화의 공간·거리·첫 3합·세 번의 역전·기능 손실
- 등장 조연의 음성·사적 목표·거절선
- 장면 전후 가치와 상태 변화

## Manuscript Output

- 원고는 `manuscript/drafts/NNN_제목.md`에 저장한다.
- EP001~EP003은 장편 초고, EP004~EP200은 완결형 압축 초고다.
- 장편 확장은 EP004부터 순서대로 진행한다.
- 사건·결말·복선 답을 임의로 추가·변경하지 않는다.
- 전체 재작성보다 필요한 장면 확장과 국소 교정을 우선한다.
- 확장 뒤 원고·연속성·음성·액션·복선 검증을 실행한다.
- 작가 승인 전 원고는 draft다.

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
python scripts/materialize_compact_manuscript_v1.py
python scripts/validate_complete_compact_manuscript_v1.py
python scripts/validate_manuscript_drafts_v3_0.py
```

## Current Status

- Design Blueprint / Setting Bible / World Bible v3.4 — 완료·동결
- 5 Act / 10 Arc / 20 Subact / 200화 기능 지도 — 완료
- EP021~EP200 Production Blueprint — 180화 / 1,080비트 완료
- 8권역 / 48거점 / 20노선 / 18세력 — 완료
- 수집품 120 / 세트 24 / 신수 18 / 조연 28 — 완료
- Complete compact manuscript — EP001~EP200, **200/200**, 총 76,198자
- Draft tier — `complete_compact_first_draft`
- Publication-ready manuscript — 미완료
- Author-approved manuscript — 0화
- Next expansion target — 제4화 「보물 도둑으로 몰리다」
