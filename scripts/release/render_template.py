from __future__ import annotations

import os
import sys
from pathlib import Path
from string import Template


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: render_template.py <template-path>")

    template_path = Path(sys.argv[1])
    rendered = Template(template_path.read_text(encoding="utf-8")).safe_substitute(os.environ)
    sys.stdout.write(rendered)


if __name__ == "__main__":
    main()
