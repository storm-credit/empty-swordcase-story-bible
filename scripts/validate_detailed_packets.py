#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
files = sorted((root / "production" / "packets").glob("*.md"))
covered: list[int] = []
errors: list[str] = []

for file in files:
    text = file.read_text(encoding="utf-8")
    numbers = [int(value) for value in re.findall(r"^## (\d+)화", text, re.M)]
    covered.extend(numbers)
    for number in numbers:
        section_match = re.search(
            rf"^## {number}화.*?(?=^## \d+화|\Z)", text, re.M | re.S
        )
        if section_match is None:
            errors.append(f"{number}: missing section")
            continue
        section = section_match.group(0)
        if len(re.findall(r"^\d+\. ", section, re.M)) < 8:
            errors.append(f"{number}: under 8 beats")
        for key in ("구체 대가", "보상", "끝 훅"):
            if key not in section:
                errors.append(f"{number}: missing {key}")

expected = list(range(41, 201))
if covered != expected:
    errors.append(
        f"coverage mismatch {covered[:3]}..{covered[-3:] if covered else []}"
    )

if errors:
    print("FAIL")
    print("\n".join(errors))
    sys.exit(1)

print("PASS: 41-200, 160 episodes, >=8 beats each")
