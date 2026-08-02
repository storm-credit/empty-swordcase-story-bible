#!/usr/bin/env python3
"""Heuristic Korean prose lint. Warnings only; never replaces human editing.

Korean is agglutinative, so eojeol count alone over-flags complete sentences and
short dialogue. Rhythm checks therefore evaluate narrative sentences separately
and require both a low eojeol count and a low character count.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

SENTENCE_SPLIT = re.compile(r"(?<=[.!?…])(?:[\"'’”)]*)\s+")
ENDING = re.compile(r"(했다|였다|있었다|없었다|된다|했다가|말했다|생각했다)[.!?…]?[\"'’”)]*$")
DIALOGUE_OPEN = tuple('“\"\'')


def sentences(text: str) -> list[str]:
    clean = re.sub(r"^#+\s.*$", "", text, flags=re.M)
    return [s.strip() for s in SENTENCE_SPLIT.split(clean) if s.strip()]


def visible_chars(sentence: str) -> int:
    return len(re.sub(r"\s+|[\"'“”‘’.,!?…]", "", sentence))


def is_dialogue(sentence: str) -> bool:
    return sentence.lstrip().startswith(DIALOGUE_OPEN)


def is_short_narrative(sentence: str) -> bool:
    if is_dialogue(sentence):
        return False
    words = len(re.findall(r"\S+", sentence))
    return words <= 5 and visible_chars(sentence) <= 12


def lint(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    ss = sentences(text)
    warnings: list[str] = []
    if not ss:
        print("No sentences found")
        return 1

    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    narrative_text = "\n\n".join(
        p
        for p in paragraphs
        if not p.lstrip().startswith(DIALOGUE_OPEN) and not p.lstrip().startswith("#")
    )
    narrative = sentences(narrative_text)
    short = sum(is_short_narrative(s) for s in narrative)
    if narrative and short / len(narrative) > 0.20:
        warnings.append(f"짧은 서술문 비율 {short / len(narrative):.1%} > 20%")

    run = 0
    run_start = 0
    for idx, sentence in enumerate(narrative, 1):
        if is_short_narrative(sentence):
            if run == 0:
                run_start = idx
            run += 1
            if run >= 3:
                warnings.append(f"{run_start}번 서술문부터 짧은 문장 3연속")
                break
        else:
            run = 0

    tiny_paras = []
    for para in paragraphs:
        stripped = para.strip()
        if stripped.startswith("#") or stripped.startswith(DIALOGUE_OPEN):
            continue
        if len(re.findall(r"\S+", stripped)) <= 2 and visible_chars(stripped) <= 14:
            tiny_paras.append(stripped)
    if len(tiny_paras) > 5:
        warnings.append(f"1~2어절 서술 독립 문단 {len(tiny_paras)}개 > 5개")

    endings: list[str] = []
    for sentence in narrative:
        match = ENDING.search(sentence)
        endings.append(match.group(1) if match else "")
    for index in range(len(endings) - 3):
        if endings[index] and len(set(endings[index : index + 4])) == 1:
            warnings.append(f"서술문 {index + 1}번부터 종결 {endings[index]} 4연속")
            break

    for paragraph_index, paragraph in enumerate(paragraphs, 1):
        paragraph_sentences = sentences(paragraph)
        if len(paragraph_sentences) >= 7 and not re.search(
            r'[“”"].+?[“”"]|\b(달렸다|잡았다|들었다|놓았다|돌렸다|밀었다|당겼다)\b',
            paragraph,
        ):
            warnings.append(f"{paragraph_index}번 문단: 7문장 이상 설명 과밀 가능성")

    print(f"{path}: {len(ss)} sentences ({len(narrative)} narrative)")
    if warnings:
        for warning in warnings:
            print("WARN:", warning)
        return 2
    print("OK: no heuristic warnings")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    raise SystemExit(lint(args.path))


if __name__ == "__main__":
    main()
