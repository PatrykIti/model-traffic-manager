from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True, slots=True)
class SuiteResult:
    suite: str
    status: str
    duration_seconds: float
    artifacts_dir: str | None
    cleanup_status: str | None
    exit_code: int


def _load_registry_module():
    module_path = ROOT / "scripts/release/validation_suite_registry.py"
    spec = importlib.util.spec_from_file_location("validation_suite_registry", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load validation_suite_registry.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def resolve_suites(selection: str) -> list[str]:
    registry = _load_registry_module()
    suites = registry.SUITES

    if selection == "all":
        return [suite.suite_id for suite in suites.values()]
    if selection == "nightly":
        return [suite.suite_id for suite in suites.values() if suite.nightly_enabled]
    if selection == "release":
        return [suite.suite_id for suite in suites.values() if suite.release_enabled]

    raise ValueError(f"Unknown selection '{selection}'.")


def find_suite_artifacts_dir(artifacts_root: Path, suite: str, started_at: float) -> Path | None:
    candidates = [
        path
        for path in artifacts_root.glob(f"{suite}-*")
        if path.is_dir() and path.stat().st_mtime >= started_at - 1
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def load_cleanup_status(artifacts_dir: Path | None) -> str | None:
    if artifacts_dir is None:
        return None
    manifest_path = artifacts_dir / "manifest.json"
    if not manifest_path.exists():
        return None
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cleanup_status = manifest.get("cleanup_status")
    return cleanup_status if isinstance(cleanup_status, str) else None


def build_summary(
    *,
    environment: str,
    selection: str,
    mode: str,
    dry_run: bool,
    artifacts_root: Path,
    results: list[SuiteResult],
) -> dict[str, object]:
    started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if dry_run:
        overall_status = "planned"
    else:
        overall_status = "passed" if all(result.exit_code == 0 for result in results) else "failed"
    return {
        "environment": environment,
        "selection": selection,
        "mode": mode,
        "dry_run": dry_run,
        "artifacts_root": str(artifacts_root),
        "generated_at": started_at,
        "overall_status": overall_status,
        "results": [asdict(result) for result in results],
    }


def print_summary(summary: dict[str, object]) -> None:
    print("\nValidation matrix summary")
    print("=========================")
    print(f"Environment: {summary['environment']}")
    print(f"Selection:   {summary['selection']}")
    print(f"Mode:        {summary['mode']}")
    print(f"Artifacts:   {summary['artifacts_root']}")
    print(f"Overall:     {summary['overall_status']}")
    print("")
    for result in summary["results"]:
        assert isinstance(result, dict)
        suite = result["suite"]
        status = result["status"]
        duration = result["duration_seconds"]
        cleanup = result["cleanup_status"] or "unknown"
        artifacts_dir = result["artifacts_dir"] or "-"
        print(
            f"- {suite}: {status} | duration={duration:.1f}s | "
            f"cleanup={cleanup} | artifacts={artifacts_dir}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", required=True)
    parser.add_argument("--selection", choices=["all", "nightly", "release"], default="all")
    parser.add_argument(
        "--mode",
        choices=["continue-on-error", "fail-fast"],
        default="continue-on-error",
    )
    parser.add_argument(
        "--artifacts-root",
        default=None,
        help="Optional root directory for suite artifacts and the aggregate summary.",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    suite_ids = resolve_suites(args.selection)
    artifacts_root = (
        Path(args.artifacts_root)
        if args.artifacts_root is not None
        else Path(os.getenv("TMPDIR", "/tmp")) / f"mtm-matrix-{int(time.time())}"
    )
    artifacts_root.mkdir(parents=True, exist_ok=True)

    results: list[SuiteResult] = []
    for suite in suite_ids:
        started_at = time.time()
        if args.dry_run:
            completed_returncode = 0
            artifacts_dir = None
            cleanup_status = None
            status = "planned"
        else:
            env = os.environ.copy()
            env["VALIDATION_ARTIFACTS_ROOT"] = str(artifacts_root)
            completed = subprocess.run(
                ["bash", "scripts/release/run_azure_test_suite.sh", suite, args.environment],
                cwd=ROOT,
                env=env,
                check=False,
            )
            completed_returncode = completed.returncode
            artifacts_dir = find_suite_artifacts_dir(artifacts_root, suite, started_at)
            cleanup_status = load_cleanup_status(artifacts_dir)
            status = "passed" if completed_returncode == 0 else "failed"
        results.append(
            SuiteResult(
                suite=suite,
                status=status,
                duration_seconds=round(time.time() - started_at, 3),
                artifacts_dir=(str(artifacts_dir) if artifacts_dir is not None else None),
                cleanup_status=cleanup_status,
                exit_code=completed_returncode,
            )
        )
        if args.mode == "fail-fast" and completed_returncode != 0:
            break

    summary = build_summary(
        environment=args.environment,
        selection=args.selection,
        mode=args.mode,
        dry_run=args.dry_run,
        artifacts_root=artifacts_root,
        results=results,
    )
    summary_path = artifacts_root / "matrix-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print_summary(summary)
    print(f"\nSummary file: {summary_path}")
    if summary["overall_status"] in {"passed", "planned"}:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
