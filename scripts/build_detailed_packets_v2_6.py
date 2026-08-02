#!/usr/bin/env python3
"""Generate 41-200 detailed production packets from compact canonical data."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "production" / "packets"
OUT.mkdir(parents=True, exist_ok=True)

SOURCE_FILES = (
    "episodes_041_080.json",
    "episodes_081_120.json",
    "episodes_121_160.json",
    "episodes_161_200.json",
)

META = {
    41: ("남독택 독안개 마을과 야생계약소", "단내가 밴 독안개, 젖은 나무다리, 약초를 삶는 놋솥, 숨소리를 적는 초록 표찰", "신수 밀매단과 허가 독점", "생명을 물건처럼 다루지 않는 법"),
    51: ("잠든 숲과 천공무고 신수 분류실", "잠든 잎이 한꺼번에 뒤집히는 소리, 향로 재, 발자국이 끊긴 이끼길, 지하 분류실의 놋쇠 번호표", "귀장회 봉인대와 합법 사냥 허가", "수집하지 않고도 책임지는 법"),
    61: ("북설원 칠촌과 얼어붙은 역참", "눈벽 사이의 좁은 길, 얼음 밑 종소리, 마른 장작 냄새, 봉화대의 붉은 재", "귀장회 파수 규정과 식량난", "공동 방어구가 한 사람의 전리품이 될 수 없는 이유"),
    71: ("북설 봉인성과 백야 설원", "밤이 오지 않는 푸른 눈밭, 끊어진 봉인선, 설각마 발굽 자국, 얼음 속 이름표", "백장의 회수대와 삭제된 기록", "봉인보다 선택권을 지키는 파수"),
    81: ("서황막 대상로와 폐분관", "입안에 씹히는 모래, 되감기는 발자국, 천막 줄의 마찰음, 비어 있는데 따라오는 전시 명패", "보물세와 길을 지우는 유물", "편리함의 대가와 상극 관리"),
    91: ("폐분관 내부 전시실과 동해문", "갈라진 유리벽, 서로 다른 방향으로 울리는 유물, 그림자에 갇힌 바람, 바닷물이 번지는 문틈", "전시실 자동 분류와 수집 강박", "하나를 놓아 관계를 살리는 법"),
    101: ("동해 부유역참과 침몰도시 외곽", "젖은 밧줄 냄새, 발밑에서 기우는 부교, 조수종, 푸른 어둠 속 떠오르는 증서 조각", "여섯 가문과 합법 낙찰권", "문서 없는 기억과 공동 소유"),
    111: ("침몰도시 중앙창고와 무명시 지하역로", "거꾸로 떠오르는 기포, 녹슨 창고문, 여섯 색 닻줄, 얼굴 없는 표지판", "독점 지분과 반복되는 침몰 기억", "소유가 아닌 위탁과 분산 책임"),
    121: ("무명시 이름시장과 기억 골목", "지워진 간판, 남의 목소리로 부르는 호객, 얼굴을 비추지 않는 거울, 이름표 태우는 종이 냄새", "이름 상인과 기억 세탁", "이름 밖에서 사람을 알아보는 법"),
    131: ("무명시 중앙 장부실과 시민광장", "층마다 다른 필체의 장부벽, 마른 먹가루, 쇠사슬 달린 서가, 이름을 외치는 시민의 메아리", "중앙 장부 관리자와 강제 칭호", "기록을 나누고 현재의 이름을 선택하는 법"),
    141: ("육도천하 분산 전장", "서로 다른 여섯 문의 바람, 급보를 나르는 봉화, 끊기는 연락끈, 권역마다 다른 열쇠의 온도", "천품 쟁탈 세력과 중앙 회수 명령", "동료에게 권한을 나누는 전쟁"),
    151: ("육도 열쇠 집결지와 천외문", "여섯 열쇠가 내는 불협화음, 갈라진 문턱, 각 권역에서 온 흙과 소금, 사람 모양으로 비는 전시칸", "백장의 중앙 봉인 논리와 무주함의 재분류", "동료들의 완성과 주인공의 소멸 가능성"),
    161: ("천외산맥과 원형 천공무고", "위아래가 바뀌는 계단, 사람을 재는 문, 움직이는 전시벽, 오래된 소독약과 돌먼지 냄새", "살아 있는 박물관의 분류 체계", "사람을 목록에서 해방시키는 법"),
    171: ("원형 무고 중앙전시실과 중앙핵", "심장처럼 뛰는 금속핵, 이름이 벗겨지는 서늘함, 과거 목소리가 겹치는 통로, 손바닥에 붙는 인장", "과거 수장의 유산과 희생 강요", "기원과 현재 인격을 분리하는 선택"),
    181: ("중앙핵 내부와 육도 분산 전장", "수천 가닥 소유선, 안쪽으로 당기는 중력, 권역별로 끊겨 들리는 종소리, 두리의 냄새길", "중앙핵과 백장의 강제 봉인", "중앙을 남기지 않는 제3의 해법"),
    191: ("붕괴하는 원형 무고와 최종 배송로", "끊어지는 금빛 선, 무너진 전시대, 여섯 방향의 새벽빛, 평범해지는 낡은 검함", "마지막 소유권 선과 붕괴 시간", "파괴가 아닌 분산 배송으로 결말을 증명"),
}

ACTIONS = {
    "서린화": "린화는 빠른 결론보다 근거와 불확실성을 공개하는 쪽을 택해 담운의 계획을 수정한다.",
    "소예란": "예란은 유물 확보보다 생명 징후를 먼저 살피고, 치료 기준에 맞지 않으면 작전을 중단시키려 한다.",
    "두리": "두리는 명령을 기다리지 않고 냄새와 바람이 가리키는 대상을 스스로 선택한다.",
    "곽무석": "무석은 획득보다 퇴로와 민간인 방어를 먼저 고정해 담운의 진입 순서를 바꾼다.",
    "진여강": "진여강은 계약의 책임 주체를 따져 합법적이지만 불편한 대안을 내놓는다.",
    "백장": "백장은 피해 규모와 재발 확률을 근거로 중앙 봉인이 가장 안전하다고 밀어붙인다.",
}


def load_rows() -> list[dict]:
    rows: list[dict] = []
    for name in SOURCE_FILES:
        path = DATA / name
        if not path.exists():
            raise FileNotFoundError(f"missing source file: {path}")
        rows.extend(json.loads(path.read_text(encoding="utf-8")))
    return sorted(rows, key=lambda row: row["episode"])


def independent_action(row: dict) -> str:
    for name in row.get("cast", [])[1:]:
        if name in ACTIONS:
            return ACTIONS[name]
    return "동행자는 담운과 다른 우선순위를 선택해 같은 목표를 다른 방법으로 밀어붙인다."


def build(rows: list[dict]) -> None:
    hooks = {row["episode"]: row["hook"] for row in rows}
    initial_hook = "두리 목의 금빛 자국이 백장의 장갑과 같은 문양이다."

    for start in range(41, 201, 10):
        location, palette, opposition, question = META[start]
        block = [
            f"# {start:03d}~{start + 9:03d}화 상세 제작 패킷",
            "",
            f"- 무대: {location}",
            f"- 감각 팔레트: {palette}",
            f"- 핵심 압박: {opposition}",
            f"- 10화 질문: {question}",
            "- 승인 기준: 각 화 8개 씬비트, 구체 대가, 직전 훅 회수, 다음 화 행동 훅",
            "",
        ]

        for row in [item for item in rows if start <= item["episode"] <= start + 9]:
            episode = row["episode"]
            previous_hook = hooks.get(episode - 1, initial_hook)
            beats = [
                f"직전 훅 `{previous_hook}`을 설명으로 넘기지 않고, 담운이 손·발·장비를 움직여 확인한다.",
                f"{palette}을 통해 {location}의 방향과 생활 규칙을 동시에 보여주며 사건의 위치를 고정한다.",
                f"{opposition}이 담운보다 먼저 행동해 선택지를 줄이고, 이번 실패가 다음 화에 남을 물리적 손실을 만든다.",
                f"담운은 기존 배달·수리·무주 판정 방식으로 `{row['goal']}`에 첫 시도를 하지만 지역 규칙 때문에 예상과 다르게 작동한다.",
                independent_action(row),
                f"보상 `{row['reward']}`을 실제 반응으로 공개하고 제한·책임을 동시에 붙인다.",
                f"`{row['choice']}`을 선택한다. 실제 대가: {row['cost']}",
                f"`{row['hook']}`을 사물의 움직임·몸의 반응·새 행동 요청으로 제시해 다음 화 첫 장면을 강제한다.",
            ]
            block.extend([
                f"## {episode}화 — {row['title']}",
                "",
                f"- 회차 기능: {row['episode_function']}",
                f"- 즉시 목표: {row['goal']}",
                f"- 등장: {', '.join(row.get('cast', []))}",
                f"- 위치: {row['location']}",
                "",
                "### 씬비트",
            ])
            block.extend(f"{index}. {beat}" for index, beat in enumerate(beats, 1))
            block.extend([
                "",
                f"- **구체 대가:** {row['cost']}",
                f"- **보상:** {row['reward']}",
                f"- **끝 훅:** {row['hook']}",
                "",
            ])

        (OUT / f"{start:03d}_{start + 9:03d}.md").write_text(
            "\n".join(block), encoding="utf-8"
        )


def main() -> None:
    rows = load_rows()
    episodes = [row["episode"] for row in rows]
    if episodes != list(range(41, 201)):
        raise SystemExit(f"coverage must be 41-200 without duplicates: {episodes[:5]} ... {episodes[-5:]}")
    build(rows)
    print("generated 16 packet files for episodes 41-200")


if __name__ == "__main__":
    main()
