from __future__ import annotations

import sys
from pathlib import Path

MERGE_CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
TAB_EXTENSIONS = {".md", ".yaml", ".yml"}


def main(argv: list[str]) -> int:
    failures: list[str] = []

    for raw_path in argv:
        path = Path(raw_path)
        if not path.exists() or path.is_dir():
            continue

        content = path.read_text(encoding="utf-8", errors="surrogateescape")
        lines = content.splitlines(keepends=True)

        if content and not content.endswith("\n"):
            failures.append(f"{path}: missing trailing newline at end of file")

        for index, line in enumerate(lines, start=1):
            stripped_newline = line.rstrip("\r\n")

            if stripped_newline.rstrip(" \t") != stripped_newline:
                failures.append(f"{path}:{index}: trailing whitespace")

            if path.suffix in TAB_EXTENSIONS and "\t" in stripped_newline:
                failures.append(
                    f"{path}:{index}: tab character is not allowed in {path.suffix} files"
                )

            for marker in MERGE_CONFLICT_MARKERS:
                if stripped_newline.startswith(marker):
                    failures.append(f"{path}:{index}: merge conflict marker detected")

    if failures:
        print("\n".join(failures))
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
