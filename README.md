# 《빈 검함으로 천하를 수집한다》 Story Bible v3.1

> **Design Complete / Arcadium-Yota Reaudit Complete / World Operability Conditional Pass / Episodes 1-2 Internal Harness Pass / Author Approval Pending**

## 현재 범위

- 5 Act / 10 Arc / 20 Subact / 200화 설계 완료
- 세계관: 8권역·48거점·18세력
- 수집 시스템: 수집품 120·세트 24·신수 18
- 회차 제작 패킷·복선 회수·거점·조연·대가 연결: 200/200
- 주요 액션 공간 프리플라이트: 47/47
- 조연 음성 카드: 28/28
- 핵심 부상·장비·권리 연속성: 45개
- Arcadium/Yota 비교 후 세계관 작동성 보강: 8권역·48거점·18세력·20노선·36비밀·120용어 운영 데이터 추가
- 원고 초고: 1~2화 작성·내부 하네스 통과
- 작가 승인 원고: 0화

## GitHub 운영 원칙

- `main`을 유일한 작업 정본으로 사용한다.
- 별도 다운로드 패키지를 기본 전달 방식으로 사용하지 않는다.
- 작업은 설계/집필 → 자동 검사 → 검수 보고서 → 커밋·푸시 순서로 진행한다.
- 초고는 `manuscript/drafts/`에 저장한다.
- 작가 승인 전에는 `draft`이며 최종 원고로 승격하지 않는다.

## AI 읽기 순서

1. `CLAUDE.md`
2. `AGENTS.md`
3. `docs/48_FINAL_PROSE_PREFLIGHT_V2_9.md`
4. `docs/49_ARCADIUM_YOTA_WORLD_BIBLE_COMPARISON.md`
5. `docs/50_WORLD_OPERATIONALITY_PATCH_V3_1.md`
6. 해당 화의 v2.7 복선 태그
7. 해당 화의 v2.8 거점·조연·대가 오버레이
8. 해당 권역·세력의 v3.1 세계 운영 데이터
9. 액션 화이면 v2.9 액션 시트
10. 등장 조연의 v2.9 음성 카드
11. 활성 연속성 상태
12. 직전 화 원고와 검수 보고서

## 원고 검증

```bash
python scripts/validate_manuscript_drafts_v3_0.py
```

현재 작성본:

- `manuscript/drafts/001_수신인_없는_검함.md`
- `manuscript/drafts/002_반_치_모자란_칼.md`
- `production/reviews/001_PROSE_AUDIT_V3_0.md`
- `production/reviews/002_PROSE_AUDIT_V3_0.md`

다음 작업 대상은 제3화 「첫 번째 수집」이다.

## v3.1 세계관 재감사

- `docs/49_ARCADIUM_YOTA_WORLD_BIBLE_COMPARISON.md`
- `production/audits/ARCADIUM_YOTA_ADOPTION_CANDIDATES.md`
- `orchestra/PM_WORLD_BIBLE_REAUDIT_AFTER_ARCADIUM.md`
- `docs/50_WORLD_OPERATIONALITY_PATCH_V3_1.md`

판정: 구조 재설계는 불필요하나 세계관은 **조건부 완성**이다. 제3화 집필 전에는 v3.1 운영 데이터와 검증기를 함께 읽는다.
