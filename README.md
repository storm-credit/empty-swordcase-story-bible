# 《빈 검함으로 천하를 수집한다》 설계 저장소 v2.7

> 상태: **Canon Architecture Complete / 200-Episode Production Packet Coverage Complete / Payoff Tagging Complete / Prose Not Drafted**  
> 범위: 본편 200화 설계와 세계관 설정집. 소설 원고는 포함하지 않는다.

## 한 줄 기획

주인을 잃은 유산의 미련과 책임을 해결해야만 수납되는 빈 검함을 얻은 역참 배달부 담운이, 무기·방어구·장신구·신수·장소의 귀로를 찾아 육도천하의 중앙 소유 체계를 해체하는 수집형 모험 무협 판타지.

## 완성 범위

- 5개 액트 / 10개 대형 아크 / 20개 서브액트 / 1~200화 회차 설계
- 장면 기능 골격 800개 + 1~40화 수동 상세 씬비트 + 41~200화 검증형 제작 패킷
- 수집품 120 / 세트 24 / 신수 18
- 권역 8 / 거점 48 / 교통 노선 20 / 세력 18 / 무공 전승 36
- 1~200화 복선·맥거핀·인물·수집품 회수 태깅
- S-Tier 8 / A-Tier 20 / 인물 7 / 핵심 장치 16 / C-Tier 200

## AI가 읽을 순서

1. `AGENTS.md`
2. `CLAUDE.md`
3. `production/continuity/PAYOFF_ARCHITECTURE_V2_7.md`
4. `data/episode_payoff_index_001_200.json`
5. 해당 10화 제작 패킷
6. 세계관·인물·수집품 정본

## PM·오케스트라

- 최종 정본 승인자: 사용자(작가)
- 실무 PM: `Synapse-PM`
- 저장소 실행: Claude Code
- 데이터·CI 검증: Codex/A10
- 복선·회수 검토: A14
- 연속성 차단: A07

## 핵심 산출물

- `PROJECT_BLUEPRINT_V2_4.md` — 작품 핵심 설계
- `production/continuity/PAYOFF_ARCHITECTURE_V2_7.md` — 장편·서브액트 회수 구조
- `data/episode_payoff_index_001_200.json` — 200화별 활성 추적축 원천
- `scripts/build_episode_payoff_tags_v2_7.py` — 전체 태그·매트릭스 생성
- `scripts/validate_episode_payoff_tags_v2_7.py` — 과밀·방치·미회수·후반 신규규칙 검사
- `docs/WRITING_HARNESS_PAYOFF_ADDENDUM_V2_7.md` — 원고에서 자연스럽게 심고 회수하는 규칙
- `orchestra/PM_PAYOFF_AUDIT_V2_7.md` — PM 최종 판정

## 검증

```bash
python scripts/build_episode_payoff_tags_v2_7.py
python scripts/validate_episode_payoff_tags_v2_7.py
python scripts/build_detailed_packets_v2_6.py
python scripts/validate_detailed_packets.py
```

## 절대 경계

- 의흔은 영혼이 아니다.
- 신수는 수납하거나 자동 상속할 수 없다.
- 담운은 과거 수장의 복제 인격이 아니다.
- 대연국은 육도 전체의 제국이 아니다.
- 열린무고는 새 중앙 소유 체계가 아니다.
- 160화 이후 새로운 S-Tier 세계법칙을 추가하지 않는다.
- 설계 모드에서는 소설 원고를 자동 작성하지 않는다.

## 현재 상태

- 세계관·설정집: 정본 사용 가능
- 5액트·20서브액트·200화 구조: 완료
- 1~200화 제작 패킷 커버리지: 완료
- 1~200화 복선·회수 태깅: 완료
- 소설 본문: 미작성
