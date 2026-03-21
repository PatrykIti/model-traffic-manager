from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PYPROJECT_PATH = ROOT / "pyproject.toml"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"

VERSION_RE = re.compile(r'(?m)^(version\s*=\s*")(\d+\.\d+\.\d+)(")$')
SEMVER_TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
CHECKBOX_RE = re.compile(r"^\s*[-*]\s*\[(?P<checked>[ xX])\]\s*(?P<label>.+?)\s*$")
HEADING_RE = re.compile(r"^\s{0,3}(?P<hashes>#{1,6})\s*(?P<title>.+?)\s*$")
BRACKET_HEADING_RE = re.compile(r"^\s*\[(?P<title>.+?)\]\s*$")
BULLET_RE = re.compile(r"^\s*[-*]\s+(?P<item>.+?)\s*$")

RELEASE_IMPACTS = ("no-release", "patch", "minor", "major")
RELEASE_IMPACT_ORDER = {impact: index for index, impact in enumerate(RELEASE_IMPACTS)}
RELEASE_CATEGORIES = (
    "Added",
    "Changed",
    "Fixed",
    "Removed",
    "Deprecated",
    "Security",
    "Breaking",
)
CATEGORY_LOOKUP = {category.lower(): category for category in RELEASE_CATEGORIES}
IGNORED_NOTE_VALUES = {"", "n/a", "na", "none", "not applicable"}
CHANGELOG_HEADER = """# Changelog

This changelog tracks released versions and public release notes for `model-traffic-manager`.

Internal task-level delivery history remains in `_docs/_CHANGELOG/`.
"""


@dataclass(frozen=True, slots=True)
class ReleaseNote:
    category: str
    text: str
    pr_number: int | None


@dataclass(frozen=True, slots=True)
class PullRequestReleaseData:
    number: int
    title: str
    url: str
    merged_at: str
    impact: str | None
    notes_by_category: dict[str, list[str]]


@dataclass(frozen=True, slots=True)
class PreparedRelease:
    release_required: bool
    version: str | None
    tag: str | None
    release_notes_path: str | None
    release_notes_body: str | None


class GitHubApiError(RuntimeError):
    pass


def normalize_heading(raw_heading: str) -> str:
    heading = raw_heading.strip()
    if heading.startswith("[") and heading.endswith("]"):
        heading = heading[1:-1]
    return heading.strip().lower()


def normalize_release_note_item(raw_item: str) -> str | None:
    item = raw_item.strip()
    if item.lower() in IGNORED_NOTE_VALUES:
        return None
    return item


def parse_pull_request_release_data(
    *,
    number: int,
    title: str,
    url: str,
    merged_at: str,
    body: str,
) -> PullRequestReleaseData:
    notes_by_category: dict[str, list[str]] = {category: [] for category in RELEASE_CATEGORIES}
    impact: str | None = None
    active_section: str | None = None
    active_category: str | None = None

    for line in body.splitlines():
        heading_match = HEADING_RE.match(line) or BRACKET_HEADING_RE.match(line)
        if heading_match is not None:
            heading = normalize_heading(heading_match.group("title"))
            if heading == "release impact":
                active_section = "impact"
                active_category = None
                continue
            if heading == "release notes":
                active_section = "notes"
                active_category = None
                continue
            if active_section == "notes" and heading in CATEGORY_LOOKUP:
                active_category = CATEGORY_LOOKUP[heading]
                continue
            active_category = None
            active_section = None
            continue

        if active_section == "impact":
            checkbox_match = CHECKBOX_RE.match(line)
            if checkbox_match is not None and checkbox_match.group("checked").lower() == "x":
                label = checkbox_match.group("label").strip().lower()
                if label in RELEASE_IMPACTS:
                    impact = label
            continue

        if active_section == "notes" and active_category is not None:
            bullet_match = BULLET_RE.match(line)
            if bullet_match is None:
                continue
            item = normalize_release_note_item(bullet_match.group("item"))
            if item is not None:
                notes_by_category[active_category].append(item)

    if all(not items for items in notes_by_category.values()):
        notes_by_category["Changed"].append(title.strip())

    if impact is None:
        impact = infer_release_impact(notes_by_category)

    return PullRequestReleaseData(
        number=number,
        title=title,
        url=url,
        merged_at=merged_at,
        impact=impact,
        notes_by_category=notes_by_category,
    )


def infer_release_impact(notes_by_category: dict[str, list[str]]) -> str:
    if notes_by_category["Breaking"]:
        return "major"
    if notes_by_category["Added"]:
        return "minor"
    if any(notes_by_category[category] for category in RELEASE_CATEGORIES if category != "Added"):
        return "patch"
    return "no-release"


def combine_release_notes(
    release_data: list[PullRequestReleaseData],
) -> dict[str, list[ReleaseNote]]:
    aggregated: dict[str, list[ReleaseNote]] = {category: [] for category in RELEASE_CATEGORIES}
    for pr in sorted(release_data, key=lambda item: item.merged_at):
        for category in RELEASE_CATEGORIES:
            for text in pr.notes_by_category[category]:
                aggregated[category].append(
                    ReleaseNote(category=category, text=text, pr_number=pr.number)
                )
    return aggregated


def select_release_impact(release_data: list[PullRequestReleaseData]) -> str:
    chosen = "no-release"
    for pr in release_data:
        pr_impact = pr.impact or "no-release"
        if RELEASE_IMPACT_ORDER[pr_impact] > RELEASE_IMPACT_ORDER[chosen]:
            chosen = pr_impact
    return chosen


def bump_version(version: str, impact: str) -> str:
    match = SEMVER_TAG_RE.match(f"v{version}")
    if match is None:
        raise ValueError(f"Unsupported semantic version '{version}'.")
    major, minor, patch = (int(match.group(index)) for index in range(1, 4))
    if impact == "patch":
        patch += 1
    elif impact == "minor":
        minor += 1
        patch = 0
    elif impact == "major":
        major += 1
        minor = 0
        patch = 0
    elif impact == "no-release":
        return version
    else:
        raise ValueError(f"Unknown release impact '{impact}'.")
    return f"{major}.{minor}.{patch}"


def update_pyproject_version(pyproject_text: str, new_version: str) -> str:
    updated_text, replacements = VERSION_RE.subn(
        rf'\g<1>{new_version}\g<3>',
        pyproject_text,
        count=1,
    )
    if replacements != 1:
        raise RuntimeError("Could not update project version in pyproject.toml")
    return updated_text


def render_release_notes_body(
    *,
    version: str,
    release_date: str,
    notes_by_category: dict[str, list[ReleaseNote]],
) -> str:
    lines = [f"## v{version} - {release_date}", ""]
    for category in RELEASE_CATEGORIES:
        notes = notes_by_category[category]
        if not notes:
            continue
        lines.append(f"### {category}")
        for note in notes:
            if note.pr_number is None:
                lines.append(f"- {note.text}")
            else:
                lines.append(f"- {note.text} (#{note.pr_number})")
        lines.append("")
    if lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def prepend_changelog_entry(changelog_text: str, entry: str) -> str:
    stripped = changelog_text.rstrip()
    if stripped.startswith(CHANGELOG_HEADER.rstrip()):
        tail = stripped.removeprefix(CHANGELOG_HEADER.rstrip()).lstrip("\n")
        if tail:
            return f"{CHANGELOG_HEADER.rstrip()}\n\n{entry.rstrip()}\n\n{tail}\n"
        return f"{CHANGELOG_HEADER.rstrip()}\n\n{entry.rstrip()}\n"
    return f"{CHANGELOG_HEADER.rstrip()}\n\n{entry.rstrip()}\n\n{stripped}\n"


def run_git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def latest_semver_tag() -> str | None:
    tags = run_git("tag", "--list", "v*", "--sort=-v:refname").splitlines()
    for tag in tags:
        candidate = tag.strip()
        if SEMVER_TAG_RE.match(candidate):
            return candidate
    return None


def git_ref_exists(ref: str) -> bool:
    completed = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", ref],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


def git_commit_in_release_window(*, commit_sha: str, latest_tag: str | None) -> bool:
    if not git_ref_exists(commit_sha):
        return False
    in_head = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit_sha, "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    ).returncode == 0
    if not in_head:
        return False
    if latest_tag is None:
        return True
    already_released = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit_sha, latest_tag],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    ).returncode == 0
    return not already_released


def github_request_json(*, url: str, token: str) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "model-traffic-manager-semantic-release",
        },
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise GitHubApiError(f"GitHub API request failed for {url}: {exc.code} {body}") from exc


def fetch_merged_pull_requests(
    *,
    repository: str,
    default_branch: str,
    github_api_url: str,
    token: str,
    latest_tag: str | None,
) -> list[PullRequestReleaseData]:
    repo_path = urllib.parse.quote(repository, safe="/")
    release_data: list[PullRequestReleaseData] = []
    page = 1
    while True:
        url = (
            f"{github_api_url}/repos/{repo_path}/pulls"
            f"?state=closed&base={urllib.parse.quote(default_branch)}"
            f"&sort=updated&direction=desc&per_page=100&page={page}"
        )
        payload = github_request_json(url=url, token=token)
        if not isinstance(payload, list) or not payload:
            break
        for pull_request in payload:
            if not isinstance(pull_request, dict):
                continue
            merged_at = pull_request.get("merged_at")
            merge_commit_sha = pull_request.get("merge_commit_sha")
            if not isinstance(merged_at, str) or not isinstance(merge_commit_sha, str):
                continue
            if not git_commit_in_release_window(commit_sha=merge_commit_sha, latest_tag=latest_tag):
                continue
            number = pull_request.get("number")
            title = pull_request.get("title")
            url = pull_request.get("html_url")
            body = pull_request.get("body") or ""
            if (
                not isinstance(number, int)
                or not isinstance(title, str)
                or not isinstance(url, str)
            ):
                continue
            release_data.append(
                parse_pull_request_release_data(
                    number=number,
                    title=title,
                    url=url,
                    merged_at=merged_at,
                    body=body,
                )
            )
        page += 1
        if page > 20:
            break
    return sorted(release_data, key=lambda item: item.merged_at)


def read_project_version() -> str:
    pyproject_text = PYPROJECT_PATH.read_text(encoding="utf-8")
    match = VERSION_RE.search(pyproject_text)
    if match is None:
        raise RuntimeError("Could not find project version in pyproject.toml")
    return match.group(2)


def prepare_release(
    *,
    repository: str,
    default_branch: str,
    github_api_url: str,
    token: str,
    output_dir: Path,
    dry_run: bool,
) -> PreparedRelease:
    current_version = read_project_version()
    latest_tag = latest_semver_tag()

    if latest_tag is None:
        release_version = current_version
        release_data = fetch_merged_pull_requests(
            repository=repository,
            default_branch=default_branch,
            github_api_url=github_api_url.rstrip("/"),
            token=token,
            latest_tag=None,
        )
        included_release_data = [pr for pr in release_data if pr.impact != "no-release"]
        if included_release_data:
            release_notes = combine_release_notes(included_release_data)
        else:
            release_notes = {
                "Added": [
                    ReleaseNote(
                        category="Added",
                        text="Initial tagged release of model-traffic-manager.",
                        pr_number=None,
                    )
                ],
                "Changed": [],
                "Fixed": [],
                "Removed": [],
                "Deprecated": [],
                "Security": [],
                "Breaking": [],
            }
    else:
        latest_version = latest_tag.removeprefix("v")
        if current_version != latest_version:
            raise RuntimeError(
                "pyproject.toml version does not match the latest release tag. "
                f"Current version is {current_version}, latest tag is {latest_tag}."
            )
        release_data = fetch_merged_pull_requests(
            repository=repository,
            default_branch=default_branch,
            github_api_url=github_api_url.rstrip("/"),
            token=token,
            latest_tag=latest_tag,
        )
        included_release_data = [pr for pr in release_data if pr.impact != "no-release"]
        release_impact = select_release_impact(included_release_data)
        if release_impact == "no-release":
            return PreparedRelease(
                release_required=False,
                version=None,
                tag=None,
                release_notes_path=None,
                release_notes_body=None,
            )
        release_version = bump_version(current_version, release_impact)
        release_notes = combine_release_notes(included_release_data)

    release_date = datetime.now(UTC).date().isoformat()
    release_notes_body = render_release_notes_body(
        version=release_version,
        release_date=release_date,
        notes_by_category=release_notes,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    release_notes_path = output_dir / f"release-notes-v{release_version}.md"
    release_notes_path.write_text(release_notes_body, encoding="utf-8")

    if not dry_run:
        pyproject_text = PYPROJECT_PATH.read_text(encoding="utf-8")
        PYPROJECT_PATH.write_text(
            update_pyproject_version(pyproject_text, release_version),
            encoding="utf-8",
        )
        changelog_text = (
            CHANGELOG_PATH.read_text(encoding="utf-8")
            if CHANGELOG_PATH.exists()
            else CHANGELOG_HEADER
        )
        CHANGELOG_PATH.write_text(
            prepend_changelog_entry(changelog_text, release_notes_body),
            encoding="utf-8",
        )

    return PreparedRelease(
        release_required=True,
        version=release_version,
        tag=f"v{release_version}",
        release_notes_path=str(release_notes_path),
        release_notes_body=release_notes_body,
    )


def write_github_outputs(output_path: Path, prepared_release: PreparedRelease) -> None:
    lines = [
        f"release_required={'true' if prepared_release.release_required else 'false'}",
        f"release_version={prepared_release.version or ''}",
        f"release_tag={prepared_release.tag or ''}",
        f"release_notes_path={prepared_release.release_notes_path or ''}",
    ]
    with output_path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--default-branch", required=True)
    parser.add_argument("--github-api-url", required=True)
    parser.add_argument("--github-output", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN must be set for semantic release preparation.")

    output_dir = (
        Path(args.output_dir)
        if args.output_dir is not None
        else Path(os.getenv("RUNNER_TEMP", os.getenv("TMPDIR", "/tmp"))) / "semantic-release"
    )
    prepared_release = prepare_release(
        repository=args.repo,
        default_branch=args.default_branch,
        github_api_url=args.github_api_url,
        token=token,
        output_dir=output_dir,
        dry_run=args.dry_run,
    )

    if args.github_output is not None:
        write_github_outputs(Path(args.github_output), prepared_release)

    if prepared_release.release_required:
        assert prepared_release.tag is not None
        print(f"Prepared release {prepared_release.tag}")
        assert prepared_release.release_notes_path is not None
        print(f"Release notes: {prepared_release.release_notes_path}")
    else:
        print("No release required.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
