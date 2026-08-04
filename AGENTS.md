# AGENTS.md — 《유물을 먹는 파천마검》 제작 오케스트라 v1.0

## Governance

- 작가: 최종 정본·원고 승인
- Synapse-PM: 단계 순서, 충돌 조정, 변경 로그, 완료 판정
- Claude Code: 저장소 반영, 문서·원고 생성, 검증 실행
- Codex/A10 관점: 데이터 누락·중복·연속성·장기 지속성 감사

설계 정본은 `reboot_v1/09_CANON_FREEZE_V1.md`와 `data/pacheon_reboot_manifest_v1.json`을 따른다.

기존 v3.4는 `LEGACY_V3_4`이며 새 원고 정본이 아니다.

## Orchestra Roles

- A01 Market Editor: 제목, 소개, 초반 10화 흡입력
- A02 Conversion Architect: 참고 기능을 독창적 구조로 변환
- A03 Myth & World Architect: 파천검 역사, 상천좌, 천명망, 지역 신화
- A04 Power-System Architect: 유물→검흔→칼 형상, 합흔, 비용
- A05 Protagonist Architect: 담운의 욕망·죄책감·능동적 선택
- A06 Party & Cast Architect: 동료 독립 목표, 합류·이탈·재합류
- A07 Continuity Blocker: 이동, 상처, 기억, 계약, 검흔 상태 거부권
- A08 Long-Form Plot Architect: 5 Act / 10 Arc / 20 Subact / 200화
- A09 Voice Editor: 인물별 말투와 감정 반응
- A10 Retention Auditor: 회차 보상, 훅, 반복 피로
- A11 Mystery Editor: 파천검/파천마검 진실 공개 순서
- A12 Combat Director: 거리, 궤적, 첫 3합, 역전, 기능 손실
- A13 Exploration Director: 유적, 환경 규칙, 발견과 이동
- A14 Payoff Editor: 본흔·관계·복선·대가 장기 회수
- A15 Blind-Spot Auditor: 클리셰, 규모 과잉, 수동성, 설정 허점

이 역할들은 실제 외부 에이전트가 별도로 실행됐다는 뜻이 아니다. 하나의 제작 오케스트라 안에서 서로 다른 검토 관점으로 사용한다.

## Canon Guardrails

다음은 변경 제안 없이 바꾸지 않는다.

- 작업 제목 《유물을 먹는 파천마검》
- 파천검/파천마검 이중 명칭
- 칼날 없는 파천검의 자루
- 담운의 유물 사냥꾼 출발
- 열두 본흔과 각 대가
- 담운이 마지막 칼날 재료라는 반전
- 청람의 계약 철회권
- EP195 파천검 일회 완성
- EP199 열두 본흔 분산
- EP200 새 유적으로 향하는 결말

## Legacy Block

새 원고에서 자동 승계하지 않는다.

- 표국 배달부
- 원래 주인 찾기와 반환
- 검함
- 소유권 행정 중심 사건
- 중앙 소유선과 여섯 책임 조각
- 기존 EP001~EP200 압축 원고의 사건과 제목

## Reboot Draft Flow

1. `CLAUDE.md`와 정본 동결 문서를 읽는다.
2. 해당 EP Blueprint와 직전 원고·검수 보고서를 읽는다.
3. A08/A10/A11이 목표·보상·훅·미스터리를 잠근다.
4. A03/A04/A13이 지역 법칙·유물 기능·탐험 규칙을 확인한다.
5. A05/A06/A09가 인물 욕망·갈등·음성을 확인한다.
6. A07이 부상·기억·계약·검흔·이동 상태를 확인한다.
7. A12가 액션 공간과 기능 손실을 설계한다.
8. 한 화를 `manuscript/reboot_v1/`에 작성한다.
9. A09/A10/A14/A15 관점으로 문장·보상·회수·맹점을 검수한다.
10. `production/reviews/reboot_v1/`에 보고서를 남긴다.
11. 자동 검증을 실행하고 커밋한다.
12. 작가 승인 후에만 final 상태로 승격한다.

## Manuscript Rules

- 담운 근접 3인칭
- 화당 4,500~5,500자 목표
- 첫 10% 안에 직전 훅 행동 회수
- 6~9개 장면 비트
- 사건·선택·비용·보상·마지막 훅 보존
- 전투는 위치와 거리를 추적 가능하게 작성
- 검흔의 대가는 다음 화까지 지속
- 동료의 독립 행동과 거부권 보존
- 설명보다 행동·피해·선택으로 설정 제시
- 특정 작품의 문체·장면·고유 설정 모사 금지

## Validation

```bash
python scripts/validate_pacheon_reboot_v1.py
```

## Current Verdict

- 리부트 콘셉트: 완료
- 세계관·설정집: 완료
- 열두 본흔 성장 시스템: 완료
- 핵심 인물·세력·권역: 완료
- 5 Act / 10 Arc / 20 Subact: 완료
- EP001~EP200 회차 Blueprint: 완료
- 복선·회수: 완료
- 시장 패키지: 완료
- 리부트 장편 원고: 0/200
- 다음 작업: EP001 「버려진 길잡이」 초고와 검수