# 《빈 검함으로 천하를 수집한다》 Story Bible v2.9

> **Canon Architecture Complete / Production Linkage Complete / Prose Preflight Complete / Manuscript Not Drafted**

## 완성 범위

- 5 Act / 10 Arc / 20 Subact / 200화
- 세계관: 8권역·48거점·18세력
- 수집 시스템: 수집품 120·세트 24·신수 18
- 회차 제작 패킷·복선 회수·거점·조연·대가 연결: 200/200
- 주요 액션 공간 프리플라이트: 47/47
- 조연 음성 카드: 28/28
- 핵심 부상·장비·권리 연속성: 45개
- 소설 원고: 미작성

## AI 읽기 순서

1. `CLAUDE.md`
2. `AGENTS.md`
3. `docs/48_FINAL_PROSE_PREFLIGHT_V2_9.md`
4. 해당 화의 v2.7 복선 태그
5. 해당 화의 v2.8 거점·조연·대가 오버레이
6. 액션 화이면 v2.9 액션 시트
7. 등장 조연의 v2.9 음성 카드
8. 활성 연속성 상태

## 최종 검증

```bash
python scripts/build_effective_episodes_v2_8.py
python scripts/validate_world_cast_cost_v2_8.py
python scripts/build_episode_payoff_tags_v2_7.py
python scripts/validate_episode_payoff_tags_v2_7.py
python scripts/build_prose_preflight_v2_9.py
python scripts/validate_prose_preflight_v2_9.py
```

설정 추가 단계는 종료됐다. 다음은 1화 초고 또는 1~10화 샘플 원고로 문체 하네스를 실전 검증하는 단계다.
