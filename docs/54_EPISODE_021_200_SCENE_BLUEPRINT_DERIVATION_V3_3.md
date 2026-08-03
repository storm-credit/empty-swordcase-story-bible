# 54. 21~200화 6비트 Production Blueprint 파생 v3.3

> 상태: **비파괴 생성기·검증기 작성 완료 / 생성 결과 검증·작가 승인 대기**

## 1. 배경

기존 저장소에는 다음이 존재한다.

- 1~200화의 제목·목표·선택·보상·훅·장소·등장인물·비용
- 21~40화의 회차당 4개 비트 제작 패킷
- 41~200화의 회차 기능 지도

그러나 `CLAUDE.md`의 집필 가능 기준은 회차당 6~10개 씬비트다. 따라서 다음을 구분한다.

- 200화 Architecture와 기능 지도: 완료
- 21~200화 6~10비트 Production Blueprint: 기존 상태에서는 미완료

## 2. v3.3 생성기

`scripts/build_episode_scene_blueprints_v3_3.py`

대상:

- EP021~EP200
- 180화
- 화당 6비트
- 총 1,080비트

기본 비트:

1. `hook_recovery` — 직전 화 훅의 행동 회수
2. `world_pressure` — 지역 운영·생활·물류 압력
3. `first_attempt` — 현재 목표를 향한 첫 실제 시도
4. `evidence_and_counterpressure` — 생활 흔적·아이템·세트·신수 사건과 반압력
5. `irreversible_choice` — 기존 `choice`와 `cost`를 사용한 비가역 선택
6. `reward_cost_and_next_hook` — 기존 `reward`와 `hook`을 행동 상태로 남김

## 3. 비파괴 원칙

생성기는 다음 원본 필드를 그대로 보존한다.

- `goal`
- `choice`
- `reward`
- `hook`
- `location`
- `cast`
- `episode_function`
- `cost`

새 사건 결말·새 생존자·새 사망자·새 핵심 정답을 만들지 않는다.

생성 결과는 다음 위치에 만들어진다.

`production/blueprints/EPISODES_021_200_SCENE_BLUEPRINT_V3_3.json`

현재 결과의 지위는 `derived_production_blueprint_candidate`이며 작가 승인 전 기존 회차 정본을 대체하지 않는다.

## 4. 세계관·설정집 연결

각 화는 필요할 때 다음 후보 사건을 참조한다.

- 수집품 첫 등장·최종 상태
- 세트 완성 시점
- 신수 주요 등장 화
- Subact incoming/outgoing cost

참조 파일:

- `data/subact_causality_overlay_v3_3.json`
- `data/collection_registry_120_v3_3.json`
- `data/set_registry_024_v3_3.json`
- `data/beast_registry_018_v3_3.json`
- `data/collection_system_governance_v3_3.json`

후보 설정이 기존 회차와 충돌하면 기존 회차를 고치지 않고 후보 참조를 제거·교체한다.

## 5. 검증기

`scripts/validate_episode_scene_blueprints_v3_3.py`

검사 항목:

- EP021~EP200 정확한 180화
- 화당 정확히 6비트
- 총 1,080비트
- 비트 번호·단계 순서
- 모든 비트에 목표·압력·행동·반응·상태 변화 존재
- 기존 8개 핵심 필드와 생성 결과의 완전 일치
- 직전 훅·직전 비용 연결
- 현재 보상·비용·다음 훅 연결
- 원고 prose 혼입 금지
- 작가 승인 전 candidate 유지

## 6. 실행

```bash
python scripts/build_episode_scene_blueprints_v3_3.py
python scripts/validate_episode_scene_blueprints_v3_3.py
```

재현성 검사:

```bash
python scripts/build_episode_scene_blueprints_v3_3.py --check
```

## 7. 완료 판정 기준

다음 두 단계를 구분한다.

### 파이프라인 완료

- 생성기 존재
- 검증기 존재
- 기존 회차 정본 보존
- 180화×6비트 생성 가능

### 공식 Production Blueprint 완료

- 생성 결과 실제 생성
- 모든 검증 통과
- 기계적 반복·장소 불일치·인물 부재 감사
- 10화 단위 국소 편집
- 작가 승인

## 8. 현재 판정

> **21~200화의 6비트 상세 설계를 자동 파생할 수 있는 파이프라인은 완료됐다. 그러나 생성 결과는 작가 승인 전 후보이며, 기존 회차별 상세 설계가 공식 완료됐다고 선언하지 않는다.**
