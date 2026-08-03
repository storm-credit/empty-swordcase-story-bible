#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "arcadium_yota_extraction.md"
OUT = ROOT / "analysis" / "arcadium_categories"

SLUGS = {
    "파일 진단": "00_FILE_DIAGNOSIS.md",
    "반복 핵심어": "01_TOP_TERMS.md",
    "작품 정체·핵심 콘셉트": "02_IDENTITY_CONCEPT.md",
    "우주론·세계법칙": "03_COSMOLOGY_WORLD_LAWS.md",
    "능력·전투 체계": "04_POWER_COMBAT.md",
    "지리·환경·이동": "05_GEOGRAPHY_TRAVEL.md",
    "역사·연대기": "06_HISTORY_CHRONICLE.md",
    "정치·법·권력": "07_POLITICS_LAW.md",
    "세력·조직": "08_FACTIONS_ORGANIZATIONS.md",
    "경제·기술·생활": "09_ECONOMY_DAILY_LIFE.md",
    "종교·신화·의례": "10_RELIGION_MYTH.md",
    "종족·생물·생태": "11_SPECIES_ECOLOGY.md",
    "인물·관계·변화선": "12_CHARACTERS_RELATIONSHIPS.md",
    "유물·자원·수집 체계": "13_ARTIFACTS_COLLECTION.md",
    "스토리·액트·회차 구조": "14_STORY_STRUCTURE.md",
    "복선·미스터리·회수": "15_FORESHADOWING_PAYOFF.md",
    "작문법·제작 하네스": "16_WRITING_HARNESS.md",
    "첫머리 샘플": "17_OPENING_SAMPLE.md",
    "끝부분 샘플": "18_ENDING_SAMPLE.md",
}


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    matches = list(re.finditer(r"^## (.+)$", text, flags=re.M))
    written: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        if title == "감지된 목차·표제":
            continue
        filename = SLUGS.get(title)
        if not filename:
            continue
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[start:end].strip() + "\n"
        (OUT / filename).write_text(
            f"# Arcadium Yota 비교 추출 — {title}\n\n" + section,
            encoding="utf-8",
        )
        written.append((filename, title))

    index_lines = [
        "# Arcadium Yota 분야별 비교 추출",
        "",
        "> 원본 대용량 소설에서 비교용 문단을 자동 추출한 파생 자료다.",
        "",
    ]
    index_lines.extend(f"- [{title}](./{filename})" for filename, title in written)
    (OUT / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"wrote {len(written)} category files")


if __name__ == "__main__":
    main()
