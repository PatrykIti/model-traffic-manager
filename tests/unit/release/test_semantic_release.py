from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_module():
    module_path = Path("scripts/release/semantic_release.py")
    spec = importlib.util.spec_from_file_location("semantic_release", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_parse_pull_request_release_data_reads_explicit_impact_and_categorized_notes() -> None:
    module = _load_module()

    body = """
## Release Impact
- [ ] patch
- [x] minor
- [ ] major

## Release Notes

### Added
- Added a dedicated AKS Redis validation suite

### Changed
- Updated the validation matrix runner to emit richer summaries
""".strip()

    release_data = module.parse_pull_request_release_data(
        number=58,
        title="Add Redis validation release notes",
        url="https://github.com/example/repo/pull/58",
        merged_at="2026-03-21T12:00:00Z",
        body=body,
    )

    assert release_data.impact == "minor"
    assert release_data.notes_by_category["Added"] == [
        "Added a dedicated AKS Redis validation suite"
    ]
    assert release_data.notes_by_category["Changed"] == [
        "Updated the validation matrix runner to emit richer summaries"
    ]


def test_parse_pull_request_release_data_supports_bracket_headings() -> None:
    module = _load_module()

    body = """
[Release Notes]
[Fixed]
- Fixed flaky AKS rollout retries
[Security]
- Hardened GitHub App token usage for release automation
""".strip()

    release_data = module.parse_pull_request_release_data(
        number=59,
        title="Harden release automation",
        url="https://github.com/example/repo/pull/59",
        merged_at="2026-03-21T13:00:00Z",
        body=body,
    )

    assert release_data.impact == "patch"
    assert release_data.notes_by_category["Fixed"] == ["Fixed flaky AKS rollout retries"]
    assert release_data.notes_by_category["Security"] == [
        "Hardened GitHub App token usage for release automation"
    ]


def test_parse_pull_request_release_data_falls_back_to_pr_title_when_notes_are_missing() -> None:
    module = _load_module()

    release_data = module.parse_pull_request_release_data(
        number=60,
        title="Refresh contributor guidance",
        url="https://github.com/example/repo/pull/60",
        merged_at="2026-03-21T14:00:00Z",
        body="",
    )

    assert release_data.impact == "patch"
    assert release_data.notes_by_category["Changed"] == ["Refresh contributor guidance"]


def test_bump_version_applies_semantic_release_impacts() -> None:
    module = _load_module()

    assert module.bump_version("0.1.0", "patch") == "0.1.1"
    assert module.bump_version("0.1.0", "minor") == "0.2.0"
    assert module.bump_version("0.1.0", "major") == "1.0.0"


def test_select_release_impact_honors_explicit_no_release_entries() -> None:
    module = _load_module()

    no_release_pr = module.parse_pull_request_release_data(
        number=61,
        title="Internal docs only",
        url="https://github.com/example/repo/pull/61",
        merged_at="2026-03-21T15:00:00Z",
        body="""
## Release Impact
- [x] no-release

## Release Notes

### Changed
- Updated internal docs only
""".strip(),
    )
    patch_pr = module.parse_pull_request_release_data(
        number=62,
        title="Fix release output",
        url="https://github.com/example/repo/pull/62",
        merged_at="2026-03-21T16:00:00Z",
        body="""
## Release Notes

### Fixed
- Fixed changelog rendering
""".strip(),
    )

    included = [
        pull_request
        for pull_request in [no_release_pr, patch_pr]
        if pull_request.impact != "no-release"
    ]

    assert module.select_release_impact(included) == "patch"
    combined = module.combine_release_notes(included)
    assert [note.text for note in combined["Changed"]] == []
    assert [note.text for note in combined["Fixed"]] == ["Fixed changelog rendering"]


def test_render_release_notes_body_groups_notes_by_category() -> None:
    module = _load_module()

    notes = {
        "Added": [
            module.ReleaseNote(
                category="Added",
                text="Added release automation",
                pr_number=61,
            )
        ],
        "Changed": [
            module.ReleaseNote(
                category="Changed",
                text="Updated PR template release notes",
                pr_number=62,
            )
        ],
        "Fixed": [],
        "Removed": [],
        "Deprecated": [],
        "Security": [],
        "Breaking": [],
    }

    body = module.render_release_notes_body(
        version="0.2.0",
        release_date="2026-03-21",
        notes_by_category=notes,
    )

    assert "## v0.2.0 - 2026-03-21" in body
    assert "### Added" in body
    assert "- Added release automation (#61)" in body
    assert "### Changed" in body
    assert "- Updated PR template release notes (#62)" in body
