# 《빈 검함으로 천하를 수집한다》 Story Bible v3.4

> **Design Blueprint / Setting Bible / World Bible Complete — Manuscript Drafting Stage**

## 최종 상태

- 5 Act / 10 Arc / 20 Subact
- 본편 200화 기능 지도 완료
- EP021~EP200 상세 Production Blueprint: 180화 / 1,080비트
- 8권역 / 48거점 / 20노선 / 18세력
- 수집품 120 / 세트 24 / 신수·탈것 18
- 실제 음성 카드 기준 조연 28명 감정·관계 작동성
- S-Tier 8 / A-Tier 20 / 캐릭터 트랙 7 / 핵심 아이템 트랙 16
- 최종 의미 감사: critical error 0 / warning 0
- 원고: 기존 1~2화 초고 외 미집필

설계도·설정집·세계관은 승인 ID `AUTHOR-AUTO-V3.4-20260803`으로 동결됐다. 이후 기본 작업은 새 설정 추가가 아니라 정본 기반 원고 집필과 인간 독자 반응에 따른 국소 편집이다.

## 최종 정본 진입점

1. `CLAUDE.md`
2. `AGENTS.md`
3. `data/project_manifest_v3_4.json`
4. `docs/57_FINAL_CANON_FREEZE_V3_4.md`
5. `COMPLETE_BLUEPRINT.md`
6. `WORLD_BIBLE_COMPLETE.md`
7. `data/effective_world_v3_4.json`
8. `data/collection_registry_120_v3_4.json`
9. `data/set_registry_024_v3_4.json`
10. `data/beast_registry_018_v3_4.json`
11. `data/supporting_cast_operability_028_v3_4.json`
12. `production/blueprints/EPISODES_021_200_SCENE_BLUEPRINT_V3_4.json`
13. 해당 화의 복선·대가·연속성·액션 자료
14. 직전 화 원고와 검수 보고서

## 보호 정본

- 담운의 현재 인격과 과거 수장으로부터의 독립성
- 신수 비소유·거절·종료·철회권
- 소유권·귀환·책임 주제
- 중앙 소유선 절단과 여섯 책임 조각 배송
- 기존 200화의 목표·선택·보상·훅·비용
- S-Tier 8개와 A-Tier 20개의 최종 답

설정 변경이 필요하면 원본을 덮어쓰지 않고 변경 이유·영향 범위·회차 연속성·복선 영향이 포함된 별도 변경 제안으로 처리한다.

## 최종 검증

```bash
python scripts/finalize_canon_v3_4_complete.py
python scripts/validate_final_canon_v3_4_complete.py
```

## 원고 운영

- 초고는 `manuscript/drafts/NNN_제목.md`에 저장한다.
- 한 번에 한 화만 작성한다.
- 해당 화 v3.4 Production Blueprint와 직전 화 종료 상태를 먼저 읽는다.
- 초고 뒤 자동 검증과 역할별 검수 보고서를 남긴다.
- 작가 승인 전 원고는 draft이며 설계 정본과 구분한다.

현재 다음 집필 대상은 제3화 「첫 번째 수집」이다.
