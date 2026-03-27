from __future__ import annotations

from pathlib import Path

import yaml


def main() -> None:
    workflow_dir = Path(".github/workflows")
    for path in sorted(workflow_dir.glob("*.yml")):
        yaml.safe_load(path.read_text(encoding="utf-8"))
        print(path)


if __name__ == "__main__":
    main()
