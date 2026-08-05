#!/usr/bin/env python3
from __future__ import annotations
import lzma
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "assets/reboot_ep003_020.tar.xz"


def safe_extract(tf: tarfile.TarFile, root: Path) -> None:
    resolved = root.resolve()
    for member in tf.getmembers():
        target = (root / member.name).resolve()
        if target != resolved and resolved not in target.parents:
            raise RuntimeError(f"unsafe archive path: {member.name}")
    tf.extractall(root)


def main() -> None:
    raw = lzma.decompress(ARCHIVE.read_bytes())
    temp = ROOT / ".ep003_020.tar"
    temp.write_bytes(raw)
    try:
        with tarfile.open(temp, mode="r:") as tf:
            safe_extract(tf, ROOT)
    finally:
        temp.unlink(missing_ok=True)
    print("materialized EP003~EP020 manuscripts, reviews, and progress metadata")


if __name__ == "__main__":
    main()
