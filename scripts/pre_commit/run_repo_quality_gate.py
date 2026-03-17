from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(command: list[str]) -> int:
    print(f"Running: {' '.join(command)}")
    completed = subprocess.run(command, cwd=ROOT)
    return completed.returncode


def tracked_shell_scripts() -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files", "*.sh"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in completed.stdout.splitlines() if line]


def main() -> int:
    pyproject = ROOT / "pyproject.toml"
    app_dir = ROOT / "app"
    tests_dir = ROOT / "tests"

    if not pyproject.exists() or not app_dir.exists() or not tests_dir.exists():
        print("Python quality gate skipped: pyproject.toml, app/, or tests/ is not available yet.")
        return 0

    shell_scripts = tracked_shell_scripts()
    commands = [
        ["bash", "-n", *shell_scripts],
        ["uv", "run", "ruff", "check", "."],
        ["uv", "run", "mypy", "app"],
        ["uv", "run", "pytest", "--cov=app", "--cov-report=term-missing", "--cov-fail-under=85"],
    ]

    for command in commands:
        if run(command) != 0:
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
