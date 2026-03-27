from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC_ROOTS = (ROOT / "docs", ROOT / "_docs")
REQUIRED_FILES = (
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / ".pre-commit-config.yaml",
    ROOT / "docs" / "README.md",
    ROOT / "_docs" / "README.md",
    ROOT / "_docs" / "_TASKS" / "README.md",
    ROOT / "_docs" / "_CHANGELOG" / "README.md",
)
NAVIGATION_REQUIRED = (
    ROOT / "AGENTS.md",
    ROOT / "CONTRIBUTING.md",
)

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def collect_markdown_files() -> list[Path]:
    markdown_files: list[Path] = []
    for doc_root in DOC_ROOTS:
        markdown_files.extend(sorted(doc_root.rglob("*.md")))
    markdown_files.extend(path for path in NAVIGATION_REQUIRED if path.exists())
    return markdown_files


def has_navigation_controls(path: Path) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines()
    probe = [line for line in lines[:5] if line.strip()]
    return any(("[" in line and "](" in line) for line in probe)


def validate_markdown_links(path: Path) -> list[str]:
    failures: list[str] = []
    content = path.read_text(encoding="utf-8")
    for target in MARKDOWN_LINK_RE.findall(content):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue

        clean_target = target.split("#", 1)[0]
        if not clean_target:
            continue

        resolved = (path.parent / clean_target).resolve()
        if target.endswith("/"):
            exists = resolved.is_dir()
        else:
            exists = resolved.exists()

        if not exists:
            failures.append(f"{path}: broken local link -> {target}")

    return failures


def main() -> int:
    failures: list[str] = []

    for required_file in REQUIRED_FILES:
        if not required_file.exists():
            failures.append(f"missing required repository file: {required_file.relative_to(ROOT)}")

    for doc_root in DOC_ROOTS:
        if not doc_root.exists():
            failures.append(f"missing documentation root: {doc_root.relative_to(ROOT)}")
            continue

        for directory in sorted(path for path in doc_root.rglob("*") if path.is_dir()):
            readme_path = directory / "README.md"
            if not readme_path.exists():
                failures.append(f"{directory.relative_to(ROOT)}: missing README.md")

    for markdown_file in collect_markdown_files():
        if markdown_file == ROOT / "README.md":
            continue

        if not has_navigation_controls(markdown_file):
            failures.append(
                f"{markdown_file.relative_to(ROOT)}: missing navigation controls near the top"
            )

        failures.extend(validate_markdown_links(markdown_file))

    if failures:
        print("\n".join(failures))
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
