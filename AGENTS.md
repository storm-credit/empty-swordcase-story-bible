# AGENTS.md — Novel Production Orchestra v3.4

## Governance

- 작가: 최종 정본·원고 승인
- Synapse-PM: 실무 PM·작업 분해·충돌 조정·승인 게이트
- Claude Code: 승인된 변경과 작업 산출물의 저장소 반영
- Codex/A10: 데이터·CI·누락·중복 검사

설계도·설정집·세계관은 승인 ID `AUTHOR-AUTO-V3.4-20260803`으로 동결됐다. 기본 작업은 원고 제작이며, 설정 확장은 별도 변경 제안이 있을 때만 수행한다.

## Orchestra

- A01 장편 구조
- A02 세계관
- A03 연재 페이싱
- A04 인물 아크·조연
- A05 수집 시스템
- A06 무협 액션
- A07 연속성 차단
- A08 독창성 레드팀
- A09 목소리·대사
- A10 제작 데이터
- A11 문장 리듬
- A12 공간·풍경
- A13 액션 안무
- A14 복선·회수
- A15 전권 편집
- A16 독자 시뮬레이션

## v3.4 Draft Flow

1. Synapse-PM이 `data/project_manifest_v3_4.json`과 해당 화 v3.4 Production Blueprint를 잠근다.
2. A01/A03이 인과·회차 보상·마지막 훅을 확인한다.
3. A02/A04/A05가 effective world·조연 작동성·수집 시스템 상태를 확인한다.
4. A07이 직전 화의 부상·장비·권리·지식·관계 상태를 확인한다.
5. 액션 화는 A12/A13의 공간·거리·역전·기능 손실 시트를 읽는다.
6. 초고 작성자는 한 화만 `manuscript/drafts/`에 작성한다.
7. A09/A11이 음성·문장 리듬·파편 문장 반복을 검사한다.
8. A14가 복선의 설치·재등장·행동 회수를 검사한다.
9. A08/A15/A16이 모방·늘어짐·독자 이탈·보상 반복을 검사한다.
10. 자동 원고 검증을 통과한 뒤 검수 보고서와 함께 커밋한다.
11. 작가 승인 후에만 최종 원고 영역으로 승격한다.

한 역할이 초고 작성과 최종 승인 판정을 동시에 맡지 않는다. 여러 외부 에이전트가 실제 실행되지 않았다면 독립 실행 완료라고 표현하지 않는다.

## Required Inputs

- `data/project_manifest_v3_4.json`
- `docs/57_FINAL_CANON_FREEZE_V3_4.md`
- `data/effective_world_v3_4.json`
- `data/collection_registry_120_v3_4.json`
- `data/set_registry_024_v3_4.json`
- `data/beast_registry_018_v3_4.json`
- `data/supporting_cast_operability_028_v3_4.json`
- 해당 화의 `production/blueprints/EPISODES_021_200_SCENE_BLUEPRINT_V3_4.json` 항목
- 해당 화의 v2.7 복선 태그
- 해당 화의 v2.8 거점·조연·대가 오버레이
- v2.9 액션·음성·연속성 자료
- 직전 화 초고와 검수 보고서

## Design Change Gate

정본 변경 제안은 다음을 모두 포함해야 한다.

- 바꾸려는 정확한 파일·ID·회차
- 기존 설정이 실패하는 이유
- 5 Act·복선·수집품·인물 아크 영향
- 최소 변경안과 대안
- 검증기 수정 여부
- 작가 승인 기록

이 절차 없이 새 지역·세력·수집품·신수·주요 인물을 추가하지 않는다.

## Current Verdict

- 설계도·설정집·세계관 v3.4: 완료·동결
- 200화 기능 지도: 완료
- EP021~EP200 상세 Blueprint: 180화 / 1,080비트 완료
- 8권역·48거점·20노선·18세력: 완료
- 수집품 120·세트 24·신수 18·조연 28: 완료
- 최종 의미 감사: 통과
- 1~2화 초고: 내부 하네스 통과
- 작가 승인 원고: 0화
- 다음 작업: 제3화 초고·검수·푸시
