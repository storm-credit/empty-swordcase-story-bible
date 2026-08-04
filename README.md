# 《유물을 먹는 파천마검》 Story Bible v1.1

> **리부트 설계 EP001~EP200 완료 / 장편 초고 EP001~EP002 완료**

## 현재 상태

- 장르: 동양 다크 모험 판타지 70 / 무협식 액션 30
- 주인공: 하급 유물 사냥꾼 담운
- 핵심 장치: 파천검의 칼날 없는 자루
- 이중 명칭: 파천검 / 파천마검
- 성장: 유물 → 검흔 → 칼 형상
- 열두 본흔·여덟 권역·핵심 파티·적대 세력 완료
- 5 Act / 10 Arc / 20 Subact 완료
- EP001~EP200 회차 Blueprint 완료
- 장편 초고: **2/200**
- 작가 승인 원고: **0/200**
- 다음 원고: EP003 「고철 한 자루」

## 작품 핵심

> 유적에서 주운 칼날 없는 자루가 기이한 유물을 삼킬 때마다 새로운 칼을 만든다. 담운은 열두 본흔을 모을수록 강해지지만, 마지막 칼이 완성되는 순간 파천마검의 칼날이 되어 사라진다.

초기 검흔:

- 화귀의 심장 → 불을 먹는 `흑염도`
- 설왕의 갑주 → 공격을 얼리는 `빙갑검`
- 공간을 접는 지도 → 거리를 베는 `공절검`
- 기억을 삼킨 거울 → 기억과 환상을 베는 `몽단검`
- 신수의 뿔 → 폭풍을 두르는 `풍아검`

## 정본 진입점

1. `CLAUDE.md`
2. `AGENTS.md`
3. `reboot_v1/09_CANON_FREEZE_V1.md`
4. `reboot_v1/01_FINAL_PREMISE.md`
5. `reboot_v1/02_WORLD_BIBLE.md`
6. `reboot_v1/03_POWER_SYSTEM.md`
7. `reboot_v1/04_CAST_AND_FACTIONS.md`
8. `reboot_v1/05_REGIONS_RELICS_AND_EXPLORATION.md`
9. `reboot_v1/06_5ACT_10ARC_20SUBACT.md`
10. `reboot_v1/07_FORESHADOWING_AND_PAYOFF.md`
11. `reboot_v1/08_MARKET_AND_SERIALIZATION_PACKAGE.md`
12. `reboot_v1/episodes/`
13. `data/pacheon_reboot_manifest_v1.json`
14. `data/reboot_manuscript_progress_v1.json`
15. `manuscript/reboot_v1/`
16. `production/reviews/reboot_v1/`

## 장편 원고

### EP001 「버려진 길잡이」

- 경로: `manuscript/reboot_v1/EP001_버려진_길잡이.md`
- 상태: `draft`
- 본문: 줄바꿈 제외 5,135자
- 핵심 사건: 적화 폐광 탐사대가 담운을 미끼로 버림
- 선택: 담운은 안전한 단독 탈출 대신 부상자와 자신을 버린 일행을 구조
- 보상: 뒤집힌 표식과 역방향 퇴로 파악
- 비용: 오른쪽 어깨·왼쪽 종아리 체온과 감각 손실
- 훅: 닫힌 석문 안에서 칼날 없는 자루가 울리며 문이 열림
- 검수: `production/reviews/reboot_v1/EP001_REVIEW.md`

### EP002 「불이 차갑다」

- 경로: `manuscript/reboot_v1/EP002_불이_차갑다.md`
- 상태: `draft`
- 본문: 줄바꿈 제외 4,792자
- 핵심 사건: 고대 대장간과 광부 대피소에서 차가운 화재의 규칙 조사
- 보상: 푸른 불꽃이 불이 아니라 살아 있는 열을 먹고 추적한다는 규칙 확정
- 비용: 기존 저체온·사지 감각 손실 지속, 손바닥 파열
- 훅: 얼어붙은 푸른 불꽃 속 생존자의 손과 목소리 발견
- 검수: `production/reviews/reboot_v1/EP002_REVIEW.md`

## 다음 회차

EP003 「고철 한 자루」

- 푸른 불꽃 속 생존자를 꺼내는 행동을 첫 10% 안에 시작
- 고대 대장간으로 돌아가 칼날 없는 자루를 챙김
- 자루가 유물의 방향을 가리키는 기능을 처음 확인
- 자루를 칼처럼 휘둘러도 칼날은 아직 나타나지 않음
- 마지막 훅: 광산 전체에서 심장 박동이 울림

## 구판 처리

기존 《빈 검함으로 천하를 수집한다》 v3.4 설계와 EP001~EP200 압축 초고는 삭제하지 않는다. 상태는 `LEGACY_V3_4`이며 새 작품의 정본이 아니다.

새 정본에서 폐기된 메인 요소:

- 표국 배달부
- 원래 주인 찾아주기
- 검함
- 소유권·반환 행정 중심 진행
- 중앙 소유선과 여섯 책임 조각 결말

## 검증

```bash
python scripts/validate_pacheon_reboot_v1.py
python scripts/validate_reboot_manuscript_v1.py
```

검증 항목:

- 설계 정본 필수 파일
- 5 Act / 10 Arc / 20 Subact / 200화
- 열두 본흔
- 완료된 원고와 검수 보고서
- 원고 분량 4,500~5,500자
- 회차 연속성과 다음 집필 대상
- 구판 금지 핵심어와 임시 토큰
