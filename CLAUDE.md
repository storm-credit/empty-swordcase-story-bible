# CLAUDE.md — Empty Swordcase Story Bible v2.8

## Mission

이 저장소는 《빈 검함으로 천하를 수집한다》의 정본 설계도·세계관·제작 관리 시스템이다. 기본 모드는 `DESIGN_MODE`이며, 사용자가 명시적으로 요청하기 전에는 소설 본문을 작성하지 않는다.

## Authority

- Final Canon Owner: 사용자(작가)
- Project Manager / Lead Story Architect: Synapse-PM
- Repository Executor: Claude Code
- Data / CI Auditor: Codex/A10
- Continuity Blocker: A07
- Foreshadowing & Payoff Editor: A14

작가 승인 없이는 주인공 정체, 신수 비소유 원칙, 5액트 결말, 주요 동료의 생존·이탈, 소유권·귀환·책임이라는 주제를 변경하지 않는다.

## Canon Reading Order

1. `CLAUDE.md`
2. `AGENTS.md`
3. `PROJECT_BLUEPRINT_V2_4.md`
4. `production/continuity/PAYOFF_ARCHITECTURE_V2_7.md`
5. `data/episode_payoff_index_001_200.json`에서 해당 화
6. `data/episode_world_cast_cost_index_001_200.json`에서 해당 화
7. 해당 `production/packets/` 10화 패킷
8. 관련 세계관·인물·수집품 정본

## Production Gate

한 화를 집필 가능 상태로 판정하려면 다음을 모두 충족해야 한다.

1. 회차 목표와 반대자 목표가 구체적이다.
2. 6~10개 씬비트가 있다.
3. 장소·인물·수집품이 정본 ID로 연결된다.
4. 실제 대가와 후속 상태가 명시된다.
5. 전투 화는 공간·거리·세 번의 역전·기능 손실을 갖는다.
6. 직전 C-Tier 훅을 첫 10%에서 행동으로 회수한다.
7. 이번 화의 S/A/CH/IT 태그가 지정돼 있다.
8. A07과 A14 검사를 통과한다.

## Payoff Gate v2.7

- S-Tier: 장편 전체 질문 8개.
- A-Tier: 10화 서브액트 추적축 20개.
- CH-Tier: 주요 인물 변화선 7개.
- IT-Tier: 핵심 수집품·제도 장치 16개.
- C-Tier: C001~C200 회차 훅.
- 핵심 복선은 40화 넘게 재등장 없이 방치하지 않는다.
- 160화 이후 새로운 S-Tier 세계법칙을 만들지 않는다.
- 정답 발표만으로 회수하지 않고 선택·관계·장비·제도 변화로 갚는다.

## Production Linkage Gate v2.8

- v2.7 회차 서사 원천에 v2.8 거점·조연·대가 오버레이를 적용한다.
- 48개 거점은 각각 최소 2회 본편에서 사용한다.
- 조연 28명의 첫 등장·재등장·종착은 `supporting_cast_ids`로 연결한다.
- 모든 화의 대가는 구체적이며 200화 사이 중복 문장을 허용하지 않는다.
- 변경 후 다음을 실행한다.

```bash
python scripts/build_effective_episodes_v2_8.py
python scripts/validate_world_cast_cost_v2_8.py
```

## Non-Negotiable Rules

- 강탈품은 정상 수납 불가.
- 신수는 소유·수납 대상이 아니다.
- 귀환·비수집·공동 책임도 도감 진척이다.
- 의흔은 영혼이 아니라 사물에 남은 행위·감정의 흔적이다.
- 단문 자체가 아니라 파편 단문의 연속을 제한한다.
- 전투는 거리·발 위치·무기 궤적·기능 손실을 추적 가능하게 쓴다.
- 풍경은 방향·생활·위험·감정·액션 준비 중 최소 두 기능을 수행한다.

## Definition of Done

- Architecture: 5 Act / 20 Subact / 200 Episode — 완료
- Production Packet Coverage: 1~200화 — 완료
- Payoff Tagging: 1~200화 — 완료
- World/Cast/Cost Linkage: 48/48, 28/28, 200/200 — 완료
- Draft: 소설 원고 — 미작성
- Revision: 문체·연속성·상업성 교정 — 미착수
