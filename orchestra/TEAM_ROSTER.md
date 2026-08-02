# Story Production Orchestra v2.4

## Authority

- **Executive Producer / Final Canon Owner:** 작가
- **Project Manager / Lead Story Architect:** Synapse-PM
- **Repository Executor:** Claude Code
- **Data & CI Auditor:** Codex

## Specialist Roster

| ID | Role | Primary responsibility | Current status |
|---|---|---|---|
| A01 | Narrative Architect | 5액트·20서브액트·200화 인과관계 | 구조 감사 완료, 21~200화 상세화 필요 |
| A02 | World Bible Editor | 권역·거점·세력·법·경제·문화 정합성 | 설정집 사용 가능, 회차 연결 보강 필요 |
| A03 | Serialization & Pacing Editor | 보상 주기·정보량·유료 구간 훅 | 구조 감사 완료 |
| A04 | Character Arc Editor | 핵심 인물 변화선·조연 재등장 | 핵심 아크 사용 가능, 조연 회차 연결 필요 |
| A05 | Collection System Designer | 수집품·세트·신수의 획득·대가·귀환 | 시스템 사용 가능, 개별 생애주기 연결 필요 |
| A06 | Martial Action Director | 전투 공간·거리·상성·역전·부상 | 무공 체계 완료, 주요 전투 시트 필요 |
| A07 | Continuity Auditor | 시간·거리·부상·소지품·복선 정합성 | 제작 패킷마다 필수 활성화 |
| A08 | Originality Red Team | 구체적 유사성·장르 치환형 모방 점검 | 각 액트 승인 전 필수 활성화 |
| A09 | Voice & Dialogue Editor | 담운 1인칭·인물별 대사·문체 | 원고 미작성으로 대기 |
| A10 | Production Data Engineer | JSON·Markdown·검증·CI | 데이터 구조와 자동 검사 담당 |

## Approval Flow

1. Synapse-PM이 10화 단위 작업 패킷을 만든다.
2. A01과 A03이 서사 구조와 연재 리듬을 검토한다.
3. A02·A04·A05·A06이 세계관·인물·수집·전투를 상세화한다.
4. A07이 시간·거리·부상·복선·소지품을 교차 감사한다.
5. A08이 독창성 레드팀을 수행한다.
6. 작가가 핵심 변경을 최종 승인한다.
7. Claude Code가 승인된 변경을 저장소에 반영한다.
8. Codex와 A10이 데이터·CI 검증을 수행한다.

## Separation of Duties

- 초안 작성자와 최종 감사자는 같을 수 없다.
- PM은 전문가 의견을 통합하지만 작가 승인 없이 핵심 정본을 바꾸지 않는다.
- Claude Code는 기획 승인권이 없고, Codex는 작품 방향 결정권이 없다.
- 원고 작성 전 Production Gate를 통과하지 못한 회차는 집필 금지다.

## Current Project Verdict

- 세계관 백과: 정본 사용 가능
- 5액트·20서브액트: 완성
- 1~200화 사건·선택·보상·훅: 구조 완성
- 1~20화 상세 씬비트: 완성
- 21~200화 상세 씬비트: 미완성
- 주요 전투 시트: 미완성
- 소설 원고: 미작성
