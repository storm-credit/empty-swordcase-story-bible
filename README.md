# 《빈 검함으로 천하를 수집한다》 Story Bible v3.4

> **Design Blueprint / Setting Bible / World Bible Complete — EP001~EP200 Compact First Draft Complete**

## 현재 상태

- 5 Act / 10 Arc / 20 Subact
- 본편 200화 기능 지도 완료
- EP021~EP200 상세 Production Blueprint: 180화 / 1,080비트
- 8권역 / 48거점 / 20노선 / 18세력
- 수집품 120 / 세트 24 / 신수·탈것 18
- 실제 음성 카드 기준 조연 28명 감정·관계 작동성
- S-Tier 8 / A-Tier 20 / 캐릭터 트랙 7 / 핵심 아이템 트랙 16
- 설계 의미 감사: critical error 0 / warning 0
- 원고 초고: **EP001~EP200, 200/200**
- 원고 본문 합계: **76,198자**
- 원고 등급: `complete_compact_first_draft`
- 출간 준비: **아님 — EP004~EP200 장편 확장·인간 독자 검토 필요**

설계도·설정집·세계관은 승인 ID `AUTHOR-AUTO-V3.4-20260803`으로 동결됐다. 200화 압축 초고도 완결됐으며 이후 기본 작업은 새 사건 추가가 아니라 회차별 장편 확장과 국소 편집이다.

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
13. `production/reviews/COMPLETE_COMPACT_MANUSCRIPT_AUDIT_V1.md`
14. 해당 화의 `manuscript/drafts/NNN_제목.md`

## 보호 정본

- 담운의 현재 인격과 과거 수장으로부터의 독립성
- 신수 비소유·거절·종료·철회권
- 소유권·귀환·책임 주제
- 중앙 소유선 절단과 여섯 책임 조각 배송
- 기존 200화의 목표·선택·보상·훅·비용
- S-Tier 8개와 A-Tier 20개의 최종 답

설정 변경이 필요하면 원본을 덮어쓰지 않고 변경 이유·영향 범위·회차 연속성·복선 영향이 포함된 별도 변경 제안으로 처리한다.

## 검증

```bash
python scripts/finalize_canon_v3_4_complete.py
python scripts/validate_final_canon_v3_4_complete.py
python scripts/materialize_compact_manuscript_v1.py
python scripts/validate_complete_compact_manuscript_v1.py
```

## 원고 운영

- 초고는 `manuscript/drafts/NNN_제목.md`에 저장한다.
- EP001~EP003은 장편 초고이며 EP004~EP200은 압축 초고다.
- 이후 EP004부터 순서대로 플랫폼 연재 분량으로 확장한다.
- 확장 시 기존 사건·결말·복선 답을 추가하거나 바꾸지 않는다.
- 작가 승인 전 원고는 draft이며 설계 정본과 구분한다.

현재 다음 편집 대상은 제4화 「보물 도둑으로 몰리다」의 장편 확장이다.
