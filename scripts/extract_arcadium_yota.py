#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "arcadium_yota.txt"
OUTPUT = ROOT / "analysis" / "arcadium_yota_extraction.md"

ENCODINGS = ("utf-8-sig", "utf-16", "utf-16-le", "utf-16-be", "cp949", "euc-kr", "latin-1")

CATEGORIES: dict[str, tuple[str, ...]] = {
    "작품 정체·핵심 콘셉트": (
        "로그라인", "한 줄", "핵심", "주제", "테마", "장르", "컨셉", "콘셉트",
        "premise", "theme", "genre",
    ),
    "우주론·세계법칙": (
        "우주", "차원", "세계 법칙", "자연법칙", "원리", "마력", "마나", "에테르",
        "신성", "영혼", "시간", "공간", "cosmology", "world law", "physics",
    ),
    "능력·전투 체계": (
        "능력", "마법", "스킬", "등급", "경지", "전투", "무기", "방어", "약점",
        "상성", "각성", "성장", "power", "combat", "rank", "skill",
    ),
    "지리·환경·이동": (
        "대륙", "지역", "도시", "마을", "행성", "지리", "기후", "환경", "생태",
        "교통", "항로", "이동", "지도", "geography", "region", "city", "travel",
    ),
    "역사·연대기": (
        "역사", "연대기", "과거", "전쟁", "멸망", "건국", "시대", "재앙", "혁명",
        "history", "chronicle", "war", "era",
    ),
    "정치·법·권력": (
        "정치", "국가", "왕국", "제국", "정부", "귀족", "의회", "법", "재판",
        "권력", "통치", "군사", "politics", "law", "empire", "government",
    ),
    "세력·조직": (
        "세력", "조직", "길드", "교단", "가문", "회사", "군단", "협회", "파벌",
        "faction", "organization", "guild", "clan",
    ),
    "경제·기술·생활": (
        "경제", "화폐", "시장", "무역", "세금", "가격", "생산", "기술", "산업",
        "생활", "음식", "주거", "직업", "economy", "trade", "technology", "daily life",
    ),
    "종교·신화·의례": (
        "종교", "신앙", "신화", "신", "교리", "의식", "의례", "장례", "금기",
        "religion", "myth", "ritual", "god",
    ),
    "종족·생물·생태": (
        "종족", "인류", "외계", "괴물", "마물", "동물", "생물", "식물", "생태",
        "race", "species", "monster", "creature", "ecology",
    ),
    "인물·관계·변화선": (
        "주인공", "등장인물", "인물", "캐릭터", "관계", "동료", "적대자", "욕망",
        "결핍", "변화", "character", "protagonist", "relationship", "arc",
    ),
    "유물·자원·수집 체계": (
        "유물", "아이템", "보물", "자원", "수집", "제작", "재료", "소유", "귀속",
        "artifact", "item", "collection", "resource", "craft",
    ),
    "스토리·액트·회차 구조": (
        "스토리", "줄거리", "플롯", "액트", "아크", "막", "회차", "에피소드",
        "전환점", "클라이맥스", "결말", "plot", "act", "episode", "climax", "ending",
    ),
    "복선·미스터리·회수": (
        "복선", "맥거핀", "미스터리", "비밀", "반전", "회수", "떡밥", "진실",
        "foreshadow", "mystery", "secret", "twist", "payoff",
    ),
    "작문법·제작 하네스": (
        "작문", "집필", "문체", "시점", "묘사", "대사", "씬", "장면", "검수",
        "하네스", "writing", "prose", "voice", "scene", "review",
    ),
}

STOPWORDS = {
    "그리고", "그러나", "하지만", "때문", "대한", "위해", "있는", "없는", "한다", "된다",
    "것이다", "있다", "없다", "이다", "하는", "에서", "으로", "에게", "까지", "부터", "또한",
    "the", "and", "that", "with", "from", "this", "into", "are", "for", "not", "world",
}


def decode_bytes(data: bytes) -> tuple[str, str]:
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return data.decode("utf-16"), "utf-16"
    if data.startswith(b"\xef\xbb\xbf"):
        return data.decode("utf-8-sig"), "utf-8-sig"

    candidates: list[tuple[float, str, str]] = []
    for encoding in ENCODINGS:
        try:
            text = data.decode(encoding)
        except UnicodeError:
            continue
        if not text:
            continue
        control = sum(1 for ch in text if ord(ch) < 32 and ch not in "\n\r\t")
        nulls = text.count("\x00")
        hangul = len(re.findall(r"[가-힣]", text))
        readable = sum(1 for ch in text if ch.isprintable() or ch in "\n\r\t")
        score = readable / max(1, len(text)) + min(hangul / max(1, len(text)), 0.35) * 2
        score -= control / max(1, len(text)) * 20
        score -= nulls / max(1, len(text)) * 30
        if encoding == "latin-1":
            score -= 0.4
        candidates.append((score, encoding, text))
    if not candidates:
        raise SystemExit("Unable to decode arcadium_yota.txt")
    _, encoding, text = max(candidates, key=lambda row: row[0])
    return text, encoding


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
    return re.sub(r"[ \t]+\n", "\n", text)


def paragraphs(text: str) -> list[str]:
    rows = [re.sub(r"\s+", " ", part).strip() for part in re.split(r"\n\s*\n", text)]
    return [row for row in rows if len(row) >= 20]


def headings(text: str) -> list[tuple[int, str]]:
    pattern = re.compile(
        r"^\s*(?:#{1,6}\s+|\d{1,3}[.)]\s+|[IVX]{1,8}[.)]\s+|[가-힣][.)]\s+|"
        r"제\s*\d+\s*(?:부|막|장|화)|【[^】]+】|\[[^\]]+\])"
    )
    out: list[tuple[int, str]] = []
    for number, line in enumerate(text.splitlines(), 1):
        clean = line.strip()
        if clean and pattern.match(clean) and len(clean) <= 180:
            out.append((number, clean))
    return out


def context_score(paragraph: str, terms: tuple[str, ...]) -> int:
    lowered = paragraph.lower()
    score = sum(lowered.count(term.lower()) for term in terms)
    if re.search(r"(?:^|\s)(?:#{1,6}|\d+[.)]|제\s*\d+\s*(?:부|막|장|화))", paragraph):
        score += 2
    if 80 <= len(paragraph) <= 1600:
        score += 1
    return score


def category_excerpts(parts: list[str], terms: tuple[str, ...]) -> list[str]:
    scored = [(context_score(part, terms), index, part) for index, part in enumerate(parts)]
    selected: list[str] = []
    seen: set[str] = set()
    total = 0
    for score, _, part in sorted(scored, reverse=True):
        if score <= 0:
            break
        key = re.sub(r"\W+", "", part[:180]).lower()
        if not key or key in seen:
            continue
        seen.add(key)
        excerpt = part if len(part) <= 1400 else part[:1400].rstrip() + "…"
        if total + len(excerpt) > 18000 or len(selected) >= 18:
            break
        selected.append(excerpt)
        total += len(excerpt)
    return selected


def top_terms(text: str) -> list[tuple[str, int]]:
    tokens = re.findall(r"[가-힣]{2,12}|[A-Za-z][A-Za-z0-9_-]{2,24}", text)
    filtered = [token for token in tokens if token.lower() not in STOPWORDS and not token.isdigit()]
    return Counter(filtered).most_common(120)


def main() -> None:
    data = SOURCE.read_bytes()
    text, encoding = decode_bytes(data)
    text = normalize(text)
    parts = paragraphs(text)
    title_rows = headings(text)
    digest = hashlib.sha256(data).hexdigest()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "# arcadium_yota 자동 구조 추출",
        "",
        "> 이 문서는 비교 분석용 파생 자료다. 원본 정본을 변경하지 않는다.",
        "",
        "## 파일 진단",
        "",
        f"- 원본 바이트: {len(data):,}",
        f"- 감지 인코딩: `{encoding}`",
        f"- 문자 수: {len(text):,}",
        f"- 줄 수: {text.count(chr(10)) + 1:,}",
        f"- 문단 수: {len(parts):,}",
        f"- SHA-256: `{digest}`",
        "",
        "## 감지된 목차·표제",
        "",
    ]
    for number, title in title_rows[:1200]:
        lines.append(f"- L{number}: {title}")
    if len(title_rows) > 1200:
        lines.append(f"- … 나머지 {len(title_rows) - 1200}개 표제 생략")

    lines.extend(["", "## 반복 핵심어", ""])
    lines.extend(f"- {term}: {count}" for term, count in top_terms(text))

    for category, terms in CATEGORIES.items():
        lines.extend(["", f"## {category}", ""])
        excerpts = category_excerpts(parts, terms)
        if not excerpts:
            lines.append("- 관련 문단을 자동 감지하지 못함.")
            continue
        for index, excerpt in enumerate(excerpts, 1):
            lines.extend([f"### 발췌 {index}", "", excerpt, ""])

    lines.extend([
        "",
        "## 첫머리 샘플",
        "",
        "```text",
        text[:5000],
        "```",
        "",
        "## 끝부분 샘플",
        "",
        "```text",
        text[-5000:],
        "```",
        "",
    ])
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
