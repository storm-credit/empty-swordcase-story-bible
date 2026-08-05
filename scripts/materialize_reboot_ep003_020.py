#!/usr/bin/env python3
from __future__ import annotations

import base64
import io
import lzma
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = sorted((ROOT / "assets").glob("ep003_020.part*.b64"))


def safe_extract(tf: tarfile.TarFile, root: Path) -> None:
    resolved = root.resolve()
    for member in tf.getmembers():
        target = (root / member.name).resolve()
        if target != resolved and resolved not in target.parents:
            raise RuntimeError(f"unsafe archive path: {member.name}")
    tf.extractall(root)


def main() -> None:
    if len(PARTS) != 10:
        raise RuntimeError(f"expected 10 payload parts, found {len(PARTS)}")

    encoded = "".join(part.read_text(encoding="utf-8").strip() for part in PARTS)
    compressed = base64.b64decode(encoded)
    raw = lzma.decompress(compressed)

    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as tf:
        safe_extract(tf, ROOT)

    print("materialized EP003~EP020 manuscripts, reviews, and progress metadata")


if __name__ == "__main__":
    main()
