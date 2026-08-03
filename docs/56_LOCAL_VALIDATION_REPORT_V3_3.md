# 56. v3.3 로컬 생성·검증 보고서

> 대상 브랜치: `agent/world-bible-integration-v3-3`
> 판정: **로컬 생성·구조 검증 통과 / GitHub Actions 원격 실행 이력 미확인 / 작가 승인 게이트 유지**

## 1. 실행 환경

공개 작업 브랜치의 최신 압축본을 별도 로컬 작업 디렉터리에 내려받아 실행했다.

기존 `main`이나 사용자 작업 트리는 수정하지 않았다.

## 2. 실행 명령과 결과

| 단계 | 명령 | 결과 |
|---|---|---|
| effective world 생성 | `python scripts/build_effective_world_v3_3.py` | 통과 |
| EP021~EP200 6비트 생성 | `python scripts/build_episode_scene_blueprints_v3_3.py` | 통과 |
| 세계·설계 통합 검사 | `python scripts/validate_world_blueprint_integration_v3_3.py --report-json data/world_blueprint_validation_report_v3_3.json` | 구조 검증 통과 |
| 180화×6비트 검사 | `python scripts/validate_episode_scene_blueprints_v3_3.py` | 통과 |
| 120·24·18 전수 구조 검사 | `python scripts/validate_collection_system_v3_3.py` | 통과 |
| 후보 정본 거버넌스 검사 | `python scripts/validate_collection_governance_v3_3.py` | 통과 |
| 기존 28명 감정 작동성 검사 | `python scripts/validate_character_operability_v3_3.py` | 통과 |

## 3. 생성 결과

로컬 실행에서 다음 산출물이 정상 생성됐다.

- `data/effective_world_v3_3.json`
- `production/blueprints/EPISODES_021_200_SCENE_BLUEPRINT_V3_3.json`
- `data/world_blueprint_validation_report_v3_3.json`

EP021~EP200 결과는 다음 조건을 만족했다.

- 180화
- 화당 6개 비트
- 총 1,080비트
- 기존 목표·선택·보상·훅·장소·등장인물·회차 기능·비용 보존
- 원고 prose 미포함
- 작가 승인 전 candidate 유지

## 4. 구조 검증 통과 범위

- 8권역
- 48거점 고유 오버레이
- 20노선 작동성 오버레이
- 18세력·25관계선
- 20 Subact 구체 인과사슬
- 수집품 CI001~CI120
- 세트 SET001~SET024
- 신수·탈것 BS001~BS018
- 기존 인물 CH001~CH028
- 아이템↔세트 상호 참조
- 세트 구성품 등장 시점과 완성 시점
- 신수 비수집·세트 부품 금지
- 사람·신수 이름 충돌 거버넌스 교정

## 5. 통과가 의미하지 않는 것

로컬 구조 검증 통과는 다음을 자동 승인하지 않는다.

- 신규 자동 생성 이름의 문학적 품질
- 신규 사적 과거의 최종 채택
- 120개 수집품의 독자 선호
- 24세트의 장기 연재 체감 차별성
- 18신수의 최종 디자인
- 1,080비트의 장면별 개성
- 작가 승인 정본 승격

## 6. 원격 CI 상태

`.github/workflows/validate-world-blueprint-v3-3.yml`을 추가하고 작업 브랜치 `push`와 PR을 실행 조건으로 지정했다.

그러나 연결된 GitHub 앱에서 workflow run 또는 commit status가 확인되지 않았다. 따라서 원격 CI가 실행됐거나 통과했다고 주장하지 않는다.

## 7. 현재 게이트

1. 후보와 기존 회차·복선·인물 생존·이탈 결과의 의미 충돌 감사
2. 120·24·18 중복 체감 감사
3. EP021~EP200 10화 단위 장면 차별화 감사
4. 신규 이름·사적 과거에 대한 작가 승인 또는 교체
5. 승인된 항목만 공식 정본으로 승격

## 8. 최종 판정

> **v3.3 세계 통합·전수 후보 레지스트리·장면 파생 파이프라인은 로컬에서 생성 및 구조 검증을 통과했다. 그러나 자동 생성 후보는 아직 작가 승인 정본이 아니며, 원격 GitHub Actions 통과도 확인되지 않았다.**
