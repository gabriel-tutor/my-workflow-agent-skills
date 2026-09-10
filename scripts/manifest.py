#!/usr/bin/env python3
"""Hash every regular file under a directory (skipping .git, node_modules, and symlinks).

Usage: manifest.py <dir> [<out.json>]     prints JSON to stdout when no output path is given
Import: from manifest import manifest     -> dict[relpath, sha256]
"""
import hashlib
import json
import sys
from pathlib import Path

SKIP = {".git", "node_modules"}


def manifest(root: Path) -> dict[str, str]:
    root = Path(root)
    out: dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if any(part in SKIP for part in rel.parts):
            continue
        if p.is_symlink() or not p.is_file():
            continue
        out[str(rel)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 1
    text = json.dumps(manifest(Path(argv[1])), indent=1, sort_keys=True)
    if len(argv) > 2:
        Path(argv[2]).write_text(text)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
