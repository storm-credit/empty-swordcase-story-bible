# World Reference Quick v3.4

## 빠른 판정

- 설계도: **완료·동결**
- 설정집: **완료·동결**
- 세계관: **완료·동결**
- 5 Act / 10 Arc / 20 Subact / 200화 기능 지도: **완료**
- EP021~EP200 상세 Blueprint: **180화 / 1,080비트 완료**
- 8권역 / 48거점 / 20노선 / 18세력: **완료**
- 수집품 120 / 세트 24 / 신수 18 / 조연 28: **완료**
- 최종 의미 감사: **critical error 0 / warning 0**
- 원고: **기존 1~2화 초고 외 미집필**

승인 ID: `AUTHOR-AUTO-V3.4-20260803`

## 먼저 볼 파일

| 용도 | 파일 |
|---|---|
| 최종 상태 | `data/project_manifest_v3_4.json` |
| 동결 보고서 | `docs/57_FINAL_CANON_FREEZE_V3_4.md` |
| 전체 설계 | `COMPLETE_BLUEPRINT.md` |
| 세계 통합본 | `data/effective_world_v3_4.json` |
| 수집품 120 | `data/collection_registry_120_v3_4.json` |
| 세트 24 | `data/set_registry_024_v3_4.json` |
| 신수·탈것 18 | `data/beast_registry_018_v3_4.json` |
| 조연 28 | `data/supporting_cast_operability_028_v3_4.json` |
| EP021~EP200 상세 설계 | `production/blueprints/EPISODES_021_200_SCENE_BLUEPRINT_V3_4.json` |
| 최종 감사 | `data/final_semantic_audit_v3_4.json` |
| 승인 장부 | `data/canon_approval_v3_4.json` |
| 장기 복선 | `data/payoff_tracks_v2_7.json` |
| 회차 복선 태그 | `data/episode_payoff_tags_001_200.json` |

## 원고 작성 규칙

1. 해당 화 Blueprint와 직전 화 종료 상태를 먼저 읽는다.
2. 기존 `goal·choice·reward·hook·cost`를 바꾸지 않는다.
3. 거점의 생활 기능·병목·세력 자원·노선 비용을 장면 행동으로 보여준다.
4. 수집품은 획득뿐 아니라 귀환·공동 관리·비수집·책임 인계로 진척시킨다.
5. 신수는 수집품·펫·담보·세트 부품처럼 다루지 않는다.
6. 조연은 담운이 없어도 자기 목표·거절선·개인 손실을 가진다.
7. 복선은 설명보다 선택·관계·장비·제도 변화로 회수한다.
8. 새 설정이 필요해 보여도 먼저 기존 v3.4 정본에서 해결책을 찾는다.

## 정본 변경 규칙

정본을 바꾸려면 정확한 파일·ID·회차, 변경 이유, 복선·인물·세계관 영향, 최소 변경안, 검증기 수정, 작가 승인이 필요하다.

## 검증

```bash
python scripts/finalize_canon_v3_4_complete.py
python scripts/validate_final_canon_v3_4_complete.py
```

## 공식 문구

> **《빈 검함으로 천하를 수집한다》의 설계도·설정집·세계관은 v3.4로 완료·동결됐다. 다음 단계는 제3화부터의 원고 집필이다.**
