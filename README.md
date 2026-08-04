# 《유물을 먹는 파천마검》 Story Bible v1.0

> **Pacheon Reboot Design Complete — 5 Acts / 10 Arcs / 20 Subacts / EP001~EP200 Blueprint Complete**

## 현재 상태

- 장르: 동양 다크 모험 판타지 70 / 무협식 액션 30
- 핵심 주인공: 하급 유물 사냥꾼 담운
- 핵심 장치: 파천검의 칼날 없는 자루
- 이중 명칭: 파천검 / 파천마검
- 유물→검흔→칼 형상 변환 시스템
- 열두 본흔 완료
- 여덟 권역 완료
- 핵심 파티·적대자 완료
- 5 Act / 10 Arc / 20 Subact 완료
- EP001~EP200 회차별 설계 완료
- 복선·미스터리·회수 지도 완료
- 제목·소개·연재 패키지 완료
- 리부트 장편 원고: 0/200

## 작품 핵심

> 유적에서 주운 칼날 없는 자루가 기이한 유물을 삼킬 때마다 새로운 칼을 만든다. 담운은 열두 본흔을 모을수록 강해지지만, 마지막 칼이 완성되는 순간 파천마검의 칼날이 되어 사라진다.

초기 승인 검흔:

- 화귀의 심장 → 불을 먹는 `흑염도`
- 설왕의 갑주 → 공격을 얼리는 `빙갑검`
- 공간을 접는 지도 → 거리를 베는 `공절검`
- 기억을 삼킨 거울 → 기억과 환상을 베는 `몽단검`
- 신수의 뿔 → 폭풍을 두르는 `풍아검`

## 정본 진입점

1. `CLAUDE.md`
2. `AGENTS.md`
3. `reboot_v1/09_CANON_FREEZE_V1.md`
4. `reboot_v1/00_ORCHESTRA_VERDICT.md`
5. `reboot_v1/01_FINAL_PREMISE.md`
6. `reboot_v1/02_WORLD_BIBLE.md`
7. `reboot_v1/03_POWER_SYSTEM.md`
8. `reboot_v1/04_CAST_AND_FACTIONS.md`
9. `reboot_v1/05_REGIONS_RELICS_AND_EXPLORATION.md`
10. `reboot_v1/06_5ACT_10ARC_20SUBACT.md`
11. `reboot_v1/07_FORESHADOWING_AND_PAYOFF.md`
12. `reboot_v1/08_MARKET_AND_SERIALIZATION_PACKAGE.md`
13. `reboot_v1/episodes/EP001_050_BLUEPRINT.md`
14. `reboot_v1/episodes/EP051_100_BLUEPRINT.md`
15. `reboot_v1/episodes/EP101_150_BLUEPRINT.md`
16. `reboot_v1/episodes/EP151_200_BLUEPRINT.md`
17. `data/pacheon_reboot_manifest_v1.json`

## 구판 처리

기존 《빈 검함으로 천하를 수집한다》 v3.4 설계와 EP001~EP200 압축 초고는 삭제하지 않는다. 다만 상태는 `LEGACY_V3_4`이며 새 작품의 정본이 아니다.

새 정본에서 폐기된 메인 요소:

- 표국 배달부
- 원래 주인 찾아주기
- 검함
- 소유권·반환 행정 중심 진행
- 중앙 소유선과 여섯 책임 조각 결말

## 구조

### Act 1 — 칼날 없는 자루

적화분지의 흑염 / 설왕의 얼음 명령

### Act 2 — 길과 기억의 대가

접힌 사막의 지도 / 기억을 먹는 섬

### Act 3 — 계약과 전쟁

폭풍의 계약 / 무게와 천둥의 내전

### Act 4 — 끊어진 관계와 부활의 유혹

해문 아래의 선택 / 인연을 자르는 황도

### Act 5 — 한 자루가 되지 않는 검

죽은 자들이 원하는 검 / 파천검의 마지막 주인

## 검증

```bash
python scripts/validate_pacheon_reboot_v1.py
```

검증 항목:

- 필수 정본 파일 존재
- 5 Act / 10 Arc / 20 Subact / 200화
- 열두 본흔 이름과 수량
- EP001~EP200 연속성
- 200개 회차 제목 중복 여부

## 원고 운영

- 새 원고 경로: `manuscript/reboot_v1/`
- 새 검수 경로: `production/reviews/reboot_v1/`
- 화당 목표: 4,500~5,500자
- 담운 근접 3인칭
- 기존 `manuscript/drafts/` 파일을 덮어쓰지 않음
- 작가 승인 전 상태는 draft

다음 제작 대상은 리부트 제1화 「버려진 길잡이」다.