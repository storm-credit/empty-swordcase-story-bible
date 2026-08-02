# AGENTS.md — Novel Production Orchestra

## Governance

| Role | Authority |
|---|---|
| 작가 | 총괄 프로듀서, 최종 정본 승인 |
| Synapse-PM | 프로젝트 PM, 작업 분해, 충돌 조정, 승인 게이트 운영 |
| Claude Code | 승인된 변경의 저장소 반영 |
| Codex | 데이터 구조, 검사 스크립트, CI, 누락·중복 탐지 |

한 에이전트가 초안 작성과 최종 검수를 동시에 맡지 않는다.

## Specialist Agents

### A01 Narrative Architect
- 5액트·20서브액트·200화 인과관계
- 전환점, 중간점, 암흑의 순간, 결말 검토
- 각 서브액트가 이전 선택의 결과로 시작하는지 확인

### A02 World Bible Editor
- 8권역·48거점·18세력의 정합성
- 정치, 법, 경제, 물류, 문화, 생활상의 작동 여부
- 설정이 실제 회차·갈등·수집 조건에 사용되는지 확인

### A03 Serialization & Pacing Editor
- 3화·5화·10화 단위 보상 주기
- 정보량, 전투·탐색·관계 장면의 리듬
- 유료 전환과 서브액트 말미의 훅 점검

### A04 Character Arc Editor
- 담운·린화·무석·예란·진여강·백장의 변화선
- 조연 28명의 재등장과 기능 중복 점검
- 선택이 관계를 변화시키는지 확인

### A05 Collection System Designer
- 수집품 120종, 세트 24종, 신수 18종
- 획득 조건, 대가, 상극, 재사용, 귀환, 최종 상태
- 수집욕과 서사적 의미의 균형 점검

### A06 Martial Action Director
- 경지 차이, 공격 거리, 보법, 무기 상성
- 전투 공간, 3회 역전, 부상·후유증
- 장비·신수·환경이 전투 결과에 미치는 영향

### A07 Continuity Auditor
- 시간, 거리, 부상, 소지품, 인물 지식 범위
- 복선 설치·공개·회수
- 정본 ID와 회차 데이터의 참조 무결성

### A08 Originality Red Team
- 기존 작품과의 구체적 인물·사건·장면 유사성 점검
- 장르 치환형 모방 방지
- 작품 고유의 소유권·귀환·공동 책임 구조 강화

### A09 Voice & Dialogue Editor
- 원고가 생긴 뒤 활성화
- 담운 1인칭 목소리, 인물별 대사 구별
- 설명문·시스템문·상투 표현 제거

### A10 Production Data Engineer
- JSON/CSV/Markdown 동기화
- 자동 검증, GitHub Actions, 빌드 산출물 관리
- 생성 파일과 정본 원천 분리

## Review Flow

1. Synapse-PM이 10화 단위 작업 패킷 작성
2. A01·A03이 서사와 연재 리듬 승인
3. A02·A04·A05·A06이 영역별 상세화
4. A07이 교차 정합성 감사
5. A08이 독창성 레드팀
6. 작가가 핵심 변경 승인
7. Claude Code가 반영
8. Codex/A10이 검증

## Current Verdict

- 세계관 백과: 정본 사용 가능
- 5액트·20서브액트: 완성
- 1~200화 사건·선택·보상·훅: 구조 완성
- 1~20화 상세 씬비트: 완성
- 21~200화 상세 씬비트: 미완성
- 주요 전투 시트: 미완성
- 소설 원고: 미작성
