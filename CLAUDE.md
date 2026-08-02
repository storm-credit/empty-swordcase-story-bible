# CLAUDE.md — Empty Swordcase Story Bible v3.0

## Mission

이 저장소는 《빈 검함으로 천하를 수집한다》의 정본 설계·세계관·제작·집필 시스템이다. 설계 단계는 종료됐고 현재는 `DRAFT_MODE`다. GitHub `main`을 유일한 작업 정본으로 사용하며, 별도 다운로드 패키지를 기본 산출물로 만들지 않는다.

## Authority

- Final Canon Owner: 사용자(작가)
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
3. `PROJECT_BLUEPRINT_V2_4.md`
4. `docs/48_FINAL_PROSE_PREFLIGHT_V2_9.md`
5. `data/episode_payoff_index_001_200.json`
6. `data/episode_world_cast_cost_*.json`
7. v2.9 액션·음성·연속성 산출물
8. 해당 10화 제작 패킷
9. 직전 화 원고와 검수 보고서

## Draft Gate

한 화를 쓰기 전에 반드시 확인한다.

- 회차 목표·반대자 목표·6~10개 씬비트
- S/A/CH/IT/C 회수 태그
- 정본 거점·조연·구체 대가
- 활성 부상·장비·권리 상태
- 액션 화의 ZONE A~E·보폭 거리·첫 3합·세 번의 역전
- 등장 조연의 음성 카드
- 직전 훅을 첫 10%에서 행동으로 회수하는 방식

## Draft Output

- 초고는 `manuscript/drafts/NNN_제목.md`에 저장한다.
- 한 번에 한 화만 작성하고 직전 화 상태를 먼저 읽는다.
- 초고 작성 뒤 `scripts/validate_manuscript_drafts_v3_0.py`를 통과한다.
- `production/reviews/NNN_PROSE_AUDIT_*.md`에 역할별 판정을 기록한다.
- 작가 승인 전 원고는 `draft`이며 핵심 정본을 바꾸지 않는다.
- 작업·검증·커밋·푸시를 현재 작업 단위 안에서 완료한다.

## Style Gate

- 파편 단문의 연속을 금지한다.
- 전투는 거리·발 위치·궤적·재질·기능 손실을 추적 가능하게 쓴다.
- 풍경은 방향·생활·위험·감정·액션 준비 중 최소 두 기능을 수행한다.
- 복선 정답은 설명보다 선택과 관계·장비·제도 변화로 회수한다.
- 특정 작가의 고유 문체를 모사하지 않는다.

## Current Status

- Architecture / Production Packets / Payoff / World-Cast-Cost Linkage / Prose Preflight — 완료
- Episode 1 Draft / Internal Harness — 완료
- Author-approved manuscript — 0화
- Next episode — 2화 「반 치 모자란 칼」
