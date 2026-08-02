#!/usr/bin/env python3
"""Heuristic Korean prose lint. Warnings only; never replaces human editing."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

SENTENCE_SPLIT = re.compile(r"(?<=[.!?…]|[다요죠네까])(?:[\"'’”)]*)\s+")
ENDING = re.compile(
    r"(했다|였다|있었다|없었다|된다|했다가|말했다|생각했다)[.!?…]?[\"'’”)]*$"
)


def sentences(text: str) -> list[str]:
    clean = re.sub(r"^#+\s.*$", "", text, flags=re.M)
    return [s.strip() for s in SENTENCE_SPLIT.split(clean) if s.strip()]


def lint(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    ss = sentences(text)
    warnings: list[str] = []

    if not ss:
        print("No sentences found")
        return 1

    word_counts = [len(re.findall(r"\S+", sentence)) for sentence in ss]
    short = sum(1 for count in word_counts if count <= 5)
    if short / len(ss) > 0.20:
        warnings.append(f"5어절 이하 문장 비율 {short / len(ss):.1%} > 20%")

    for index in range(len(word_counts) - 2):
        if all(count <= 7 for count in word_counts[index : index + 3]):
            warnings.append(f"{index + 1}번 문장부터 7어절 이하 3연속")
            break

    tiny_paragraphs = [
        paragraph
        for paragraph in re.split(r"\n\s*\n", text)
        if 0 < len(re.findall(r"\S+", paragraph)) <= 2
    ]
    if len(tiny_paragraphs) > 5:
        warnings.append(f"1~2어절 독립 문단 {len(tiny_paragraphs)}개 > 5개")

    endings: list[str] = []
    for sentence in ss:
        match = ENDING.search(sentence)
        endings.append(match.group(1) if match else "")

    for index in range(len(endings) - 3):
        if endings[index] and len(set(endings[index : index + 4])) == 1:
            warnings.append(f"{index + 1}번 문장부터 종결 {endings[index]} 4연속")
            break

    for paragraph_index, paragraph in enumerate(re.split(r"\n\s*\n", text), 1):
        paragraph_sentences = sentences(paragraph)
        if len(paragraph_sentences) >= 7 and not re.search(
            r'[“”"].+?[“”"]|\b(달렸다|잡았다|들었다|놓았다|돌렸다|밀었다|당겼다)\b',
            paragraph,
        ):
            warnings.append(f"{paragraph_index}번 문단: 7문장 이상 설명 과밀 가능성")

    print(f"{path}: {len(ss)} sentences")
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
