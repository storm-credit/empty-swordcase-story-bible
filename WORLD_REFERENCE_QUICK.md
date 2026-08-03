# World Reference Quick v3.3

## 빠른 판정

- 작품 정체성·세계법칙: **완료**.
- 5 Act / 20 Subact / 200화 기능 지도: **완료**.
- 200화 상세 장면 설계: **미완료**.
  - 1~20화: 기존 정본 기준 완료.
  - 21~40화: 회차당 4비트, 6~10비트 게이트 미달.
  - 41~200화: 기능표만 존재.
- 8권역: **완료**.
- 48거점·20노선·18세력 통합: **v3.3 보강 완료**.
- 수집품 120·세트 24·신수 18: **전수 후보 작성 완료, 검증·충돌 감사·작가 승인 대기**.

## 반드시 먼저 볼 파일

| 용도 | 파일 |
|---|---|
| 전체 설계 | `PROJECT_BLUEPRINT_V2_4.md` |
| v3.3 통합 판정 | `docs/52_WORLD_BIBLE_BLUEPRINT_INTEGRATION_AUDIT_V3_3.md` |
| 수집 시스템 전수 후보 | `docs/53_COLLECTION_SYSTEM_REGISTRY_V3_3.md` |
| 완료 상태표 | `data/world_blueprint_completion_manifest_v3_3.json` |
| 남은 갭 | `data/world_integration_gap_register_v3_3.json` |
| 8권역 | `data/world_regions_008.json` |
| 48거점 원본 | `data/world_settlements_048.json` |
| 48거점 고유 기능 | `data/settlement_identity_overlay_v3_3.json` |
| 20노선 원본 | `data/world_routes_020.json` |
| 20노선 물류 보강 | `data/route_operability_overlay_v3_3.json` |
| 18세력 원본 | `data/world_factions_018.json` |
| 18세력 관계망 | `data/faction_relation_overlay_v3_3.json` |
| 20 Subact 원본 | `data/acts_subacts_005_020.json` |
| 20 Subact 인과사슬 | `data/subact_causality_overlay_v3_3.json` |
| 수집품 120 후보 | `data/collection_registry_120_v3_3.json` |
| 세트 24 후보 | `data/set_registry_024_v3_3.json` |
| 신수·탈것 18 후보 | `data/beast_registry_018_v3_3.json` |
| 후보 정본 보호 | `data/collection_system_governance_v3_3.json` |
| 장기 복선 | `data/payoff_tracks_v2_7.json` |
| 세계 통합 검증 | `scripts/validate_world_blueprint_integration_v3_3.py` |
| 수집 전수 검증 | `scripts/validate_collection_system_v3_3.py` |
| 후보 거버넌스 검증 | `scripts/validate_collection_governance_v3_3.py` |

## 사용 규칙

1. 거점 장면을 만들 때 원본 거점 파일과 v3.3 거점 오버레이를 함께 읽는다.
2. 이동 장면은 노선 오버레이의 처리량·폐쇄조건·우회로·연쇄손실을 사용한다.
3. 세력은 담운의 등장 전에도 관계망의 격화 조건에 따라 움직인다.
4. Subact 시작 시 이전 구간의 `outgoing_cost`를 현재 `incoming_cost`로 회수한다.
5. 120·24·18 후보 중 기존 확정 요소가 아닌 신규 이름은 작가 승인 전 원고에서 확정 설정처럼 사용하지 않는다.
6. 신수는 어떤 경우에도 수집품·담보·세트 부품으로 등록하지 않는다.
7. 후보와 기존 회차·복선이 충돌하면 기존 정본을 유지하고 후보만 수정한다.

## 현재 공식 문구

> **핵심 정본 완료 / 5액트·20서브액트·200화 기능 구조 완료 / 8권역 완료 / 48거점·20노선·18세력 통합 보강 완료 / 120수집품·24세트·18신수 전수 후보 작성 완료·검증 및 작가 승인 대기 / 200화 상세 장면 설계 미완료.**
