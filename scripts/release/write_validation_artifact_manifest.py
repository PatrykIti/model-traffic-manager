from __future__ import annotations

import json
import sys
from pathlib import Path


def build_manifest(
    artifacts_dir: Path,
    *,
    suite: str,
    environment: str,
    run_id: str,
    scope_dir: str,
    tests_path: str,
    suite_kind: str,
    exit_code: int,
    cleanup_status: str,
) -> dict[str, object]:
    files: dict[str, str] = {}
    for path in sorted(artifacts_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.name == "manifest.json":
            continue
        relative = path.relative_to(artifacts_dir).as_posix()
        files[relative.replace("/", "__")] = relative

    return {
        "suite": suite,
        "environment": environment,
        "run_id": run_id,
        "scope_dir": scope_dir,
        "tests_path": tests_path,
        "suite_kind": suite_kind,
        "exit_code": exit_code,
        "cleanup_status": cleanup_status,
        "files": files,
    }


def main() -> None:
    if len(sys.argv) != 10:
        raise SystemExit(
            "Usage: write_validation_artifact_manifest.py "
            "<artifacts-dir> <suite> <environment> <run-id> <scope-dir> "
            "<tests-path> <suite-kind> <exit-code> <cleanup-status>"
        )

    artifacts_dir = Path(sys.argv[1])
    suite = sys.argv[2]
    environment = sys.argv[3]
    run_id = sys.argv[4]
    scope_dir = sys.argv[5]
    tests_path = sys.argv[6]
    suite_kind = sys.argv[7]
    exit_code = int(sys.argv[8])
    cleanup_status = sys.argv[9]

    artifacts_dir.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest(
        artifacts_dir,
        suite=suite,
        environment=environment,
        run_id=run_id,
        scope_dir=scope_dir,
        tests_path=tests_path,
        suite_kind=suite_kind,
        exit_code=exit_code,
        cleanup_status=cleanup_status,
    )
    (artifacts_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
