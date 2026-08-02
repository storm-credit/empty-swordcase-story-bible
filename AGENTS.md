# AGENTS.md — Novel Production Orchestra v2.8

## Governance

| Role | Authority |
|---|---|
| 작가 | 총괄 프로듀서, 최종 정본 승인 |
| Synapse-PM | 작업 분해, 충돌 조정, 승인 게이트 운영 |
| Claude Code | 승인된 변경의 저장소 반영 |
| Codex/A10 | 데이터·CI·누락·중복 검사 |

한 에이전트가 초안 작성과 최종 검수를 동시에 맡지 않는다. 별도 실행 로그가 없는 경우 여러 외부 에이전트가 실제 실행됐다고 표현하지 않는다.

## Specialist Agents

- A01 Narrative Architect — 5액트·20서브액트·200화 인과관계
- A02 World Bible Editor — 지역·정치·법·경제·생활 작동성
- A03 Serialization Editor — 3화·5화·10화 보상과 훅
- A04 Character Arc Editor — 핵심 인물과 조연의 선택·관계 변화
- A05 Collection System Designer — 수집품·세트·신수의 기능·대가·귀환
- A06 Martial Action Director — 거리·보법·무기 상성·부상
- A07 Continuity Auditor — 시간·거리·지식·복선·소지품 연속성
- A08 Originality Red Team — 구체적 모방과 장르 치환 복제 방지
- A09 Voice & Dialogue Editor — 담운 1인칭과 인물별 대사
- A10 Production Data Engineer — JSON·Markdown·CI 동기화
- A11 Sentence Rhythm Editor — 파편 단문·종결 반복·설명 과밀
- A12 Space & Landscape Editor — 방향·생활·위험·액션 준비
- A13 Combat Choreographer — 전투 공간, 세 번의 역전, 기능 손실
- A14 Foreshadowing & Payoff Editor — S/A/CH/IT/C 태그와 행동 회수
- A15 Full-Volume Editor — 전권 중복·늘어짐·중반 침체
- A16 Reader Simulation — 기대·보상·이탈 지점 점검

## Review Flow

1. Synapse-PM이 10화 작업 패킷을 지정한다.
2. A01·A03이 구조와 연재 리듬을 승인한다.
3. A02·A04·A05·A06·A12·A13이 영역별 상세화를 수행한다.
4. A14가 복선·맥거핀·결말 회수를 배정한다.
5. A07이 교차 정합성을 검사한다.
6. A08이 독창성 레드팀을 수행한다.
7. 작가가 A급 변경을 승인한다.
8. Claude Code가 반영하고 Codex/A10이 검증한다.

## Required Inputs

- `production/continuity/PAYOFF_ARCHITECTURE_V2_7.md`
- `data/episode_payoff_index_001_200.json`
- `data/episode_world_cast_cost_index_001_200.json`
- `data/supporting_cast_028.json`
- `docs/WRITING_HARNESS_PAYOFF_ADDENDUM_V2_7.md`
- `docs/45_SETTLEMENT_CAST_COST_ALLOCATION_V2_8.md`
- 해당 10화 제작 패킷

## v2.8 Linkage Responsibilities

- A02: 48개 거점의 회차 사용과 지역 생활 규칙 승인.
- A04: 조연 28명의 첫 등장·재등장·종착 승인.
- A03: 신규 고유명사 과밀과 재방문 간격 검토.
- A07: 장소·부상·권리·관계 잔여 상태 교차 검사.
- A10: 48/48, 28/28, 200/200 자동 차단 검증.

## Hard Constraints

- 살아 있는 신수를 강제로 수집하지 않는다.
- 강탈품은 무주함에 정상 수납되지 않는다.
- 160화 이후 새로운 S-Tier 세계법칙을 추가하지 않는다.
- 기존 작품의 구체적 인물 역할·사건 순서·장면·반전을 복제하지 않는다.
- 특정 작가의 고유 문체를 모사하지 않고 독자 기능만 참고한다.

## Current Verdict

- 세계관 백과: 정본 사용 가능
- 5액트·20서브액트·200화 구조: 완료
- 1~200화 제작 패킷 커버리지: 완료
- 1~200화 복선·회수 태깅: 완료
- 거점 48/48·조연 28/28·구체 대가 200/200: 완료
- 소설 원고: 미작성
