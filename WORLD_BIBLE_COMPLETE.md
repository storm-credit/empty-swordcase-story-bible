# World Bible v3.3 — 통합 보강 상태

> 판정: **핵심 법칙 완료 / 8권역 완료 / 48거점·20노선·18세력 통합 보강 완료 / 120·24·18 전수 후보 작성 완료·검증 및 작가 승인 대기**.

## 1. 핵심 세계법칙 — 완료

- 무주함은 무주 상태가 확인된 사물만 정상 수납한다.
- 강탈품은 거부하거나 내부에서 폭주한다.
- 상극 유산을 함께 쓰면 기억·감각·후회·장비 기능 손실이 발생한다.
- 의흔은 영혼이 아니라 사물에 남은 행위·감정·실패의 흔적이다.
- 귀환·공동 관리·비수집도 도감 진척으로 인정된다.
- 신수는 수집품이나 펫이 아니며, 계약은 상호 동의와 철회권을 가진다.

## 2. 세계 규모와 정본 파일

- 8권역: `data/world_regions_008.json`
- 48거점 원본: `data/world_settlements_048.json`
- 48거점 고유 기능: `data/settlement_identity_overlay_v3_3.json`
- 20노선 원본: `data/world_routes_020.json`
- 20노선 물류 보강: `data/route_operability_overlay_v3_3.json`
- 18세력 원본: `data/world_factions_018.json`
- 18세력 관계망: `data/faction_relation_overlay_v3_3.json`
- 작가용 비밀 36개: `data/world_secrets_036.json`
- 정본 용어 120개: `data/world_glossary_120.json`

## 3. v3.3 세계 통합

### 48거점

기존 48거점은 이름·회차·랜드마크는 달랐지만 같은 권역의 여섯 거점이 생활 규칙·행정 일정·병목·재난·감각을 반복했다.

v3.3에서는 모든 거점에 다음을 개별 지정했다.

- 생활·행정 기능
- 지역 병목
- 반복 일상
- 소유권 분쟁
- 생활 흔적 증거
- 실패 연쇄
- 연결 노선과 주 세력

### 20노선

다음을 추가했다.

- 통제 세력
- 이동 시간
- 처리 용량
- 폐쇄 조건
- 우회로
- 연쇄 손실
- 노선별 소유권 질문

### 18세력

다음을 추가했다.

- 승리·패배 조건
- 담운 부재 시 자율 행동
- 주 활동 거점
- 25개 동맹·적대·의존·지휘 관계
- 분쟁 자원과 격화 조건

## 4. 수집 시스템 전수 후보

### 수집품 120

`data/collection_registry_120_v3_3.json`

- 20 Subact×6개
- ID·첫 등장·기능 역할·대가 축
- 획득·사용·공동 관리·귀환·비수집·책임 인계
- 세트 참조·핵심 트랙 참조·최종 상태
- 생명체 제외

### 세트 24

`data/set_registry_024_v3_3.json`

- 구성품
- 발동 조건
- 독자 보상
- 상극·관계·생활 대가
- 해체 조건
- 소유 방식
- 최종 상태

### 신수·탈것 18

`data/beast_registry_018_v3_3.json`

- 독립 목표
- 동의 조건
- 거절 조건
- 철회·이탈 조건
- 인간 이익과 인간 비용
- 주요 등장 화와 최종 상태

신수는 수집품이나 세트 부품이 될 수 없다.

## 5. 정본 거버넌스

`data/collection_system_governance_v3_3.json`이 세 후보 레지스트리보다 우선한다.

- 기존 확정 핵심 요소: 보호 정본
- 자동 생성 신규 이름·세부 기능: provisional
- 원고에서 승인 전 확정 사용: 금지
- 공식 정본 승격: 작가 승인 필요

따라서 “전수 후보가 작성됐다”와 “작가 승인 공식 정본이다”를 구분한다.

## 6. 세계 작동성 원칙

> 평시 운영 결정
> → 특정 집단 이익
> → 다른 집단 생활 손실
> → 노선·행정 병목
> → 세력 간 충돌
> → 담운의 비요청 선택
> → 다음 거점·Subact 비용

구체 데이터는 다음을 함께 읽는다.

- `data/settlement_identity_overlay_v3_3.json`
- `data/route_operability_overlay_v3_3.json`
- `data/faction_relation_overlay_v3_3.json`
- `data/subact_causality_overlay_v3_3.json`

## 7. 검증

```bash
python scripts/build_effective_world_v3_3.py
python scripts/validate_world_blueprint_integration_v3_3.py
python scripts/validate_collection_system_v3_3.py
python scripts/validate_collection_governance_v3_3.py
```

## 8. 공식 판정

- 세계 핵심 법칙: **완료**.
- 8권역: **완료**.
- 48거점·20노선·18세력 통합: **v3.3 보강 완료**.
- 수집품 120·세트 24·신수 18 전수 구조: **후보 작성 완료**.
- 신규 후보의 공식 정본 승격: **자동 검증·충돌 감사·작가 승인 대기**.
- 세계 전체의 원고 작동성: **실제 회차에서 검증 필요**.

상세 판정은 `docs/52_WORLD_BIBLE_BLUEPRINT_INTEGRATION_AUDIT_V3_3.md`, `docs/53_COLLECTION_SYSTEM_REGISTRY_V3_3.md`, `data/world_blueprint_completion_manifest_v3_3.json`을 따른다.
