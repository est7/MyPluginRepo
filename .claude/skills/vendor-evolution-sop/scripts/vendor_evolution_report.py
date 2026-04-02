#!/usr/bin/env python3
"""Generate a structured evidence report from vendor submodule diffs.

Outputs discovery-oriented evidence buckets (not conclusions) for each
updated vendor, ranked by coverage priority for deep reading.
"""

from __future__ import annotations

import argparse
import logging
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

LOGGER = logging.getLogger("vendor_evolution_report")

# Entry-point / executable filename patterns
ENTRY_FILE_PATTERNS = [
    re.compile(r"(^|/)main\.\w+$"),
    re.compile(r"(^|/)cli\.\w+$"),
    re.compile(r"(^|/)index\.\w+$"),
    re.compile(r"(^|/)(Makefile|justfile|Taskfile\.ya?ml)$"),
    re.compile(r"(^|/)__main__\.py$"),
]

# Path patterns indicating script/bin directories
SCRIPT_DIR_PATTERNS = re.compile(r"(^|/)(bin|scripts?|tools?)/")

# Max files to list per section to avoid overwhelming output
MAX_DEEP_READ_CANDIDATES = 15
MAX_FILES_PER_BUCKET = 30


@dataclass
class FileStats:
    """Per-file diff statistics."""

    path: str
    added: int = 0
    deleted: int = 0
    touch_count: int = 0
    is_new: bool = False
    is_renamed: bool = False
    rename_from: str = ""
    is_executable: bool = False

    @property
    def churn(self) -> int:
        return self.added + self.deleted


@dataclass
class VendorEvidence:
    """Structured evidence buckets for one vendor."""

    path: str
    old_sha: str
    new_sha: str
    commits: list[str] = field(default_factory=list)
    all_changed_files: list[str] = field(default_factory=list)
    new_paths: list[str] = field(default_factory=list)
    renamed_paths: list[tuple[str, str]] = field(default_factory=list)
    largest_churn_files: list[FileStats] = field(default_factory=list)
    executable_or_entry_files: list[str] = field(default_factory=list)
    repeatedly_touched_files: list[tuple[str, int]] = field(default_factory=list)
    deep_read_candidates: list[str] = field(default_factory=list)


def run(cmd: list[str], cwd: Path | None = None) -> str:
    LOGGER.debug("Running: %s", " ".join(cmd))
    try:
        completed = subprocess.run(
            cmd, cwd=cwd, check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as exc:
        LOGGER.error("Command failed: %s", " ".join(cmd))
        if exc.stderr:
            LOGGER.error(exc.stderr.strip())
        raise
    return completed.stdout


def run_no_fail(cmd: list[str], cwd: Path | None = None) -> str:
    """Like run() but returns empty string on failure instead of raising."""
    try:
        return run(cmd, cwd)
    except subprocess.CalledProcessError:
        return ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a structured evidence report for changed vendor submodules."
    )
    parser.add_argument("--base", required=True, help="Base root commit/ref")
    parser.add_argument("--head", required=True, help="Head root commit/ref")
    parser.add_argument(
        "--write",
        help="Write the markdown report to this path instead of stdout",
    )
    parser.add_argument(
        "vendors",
        nargs="*",
        help="Optional vendor paths like vendor/gstack. Defaults to all changed vendors.",
    )
    return parser.parse_args()


def changed_vendor_gitlinks(base: str, head: str) -> list[tuple[str, str, str]]:
    output = run(
        ["git", "diff", "--raw", "--no-abbrev", base, head, "--", "vendor"]
    ).splitlines()
    results: list[tuple[str, str, str]] = []
    for line in output:
        if "\t" not in line:
            continue
        meta, path = line.split("\t", 1)
        parts = meta.split()
        if len(parts) < 5:
            continue
        old_sha = parts[2]
        new_sha = parts[3]
        if not path.startswith("vendor/"):
            continue
        if old_sha == "0" * 40 or new_sha == "0" * 40:
            LOGGER.info("Skipping add/delete vendor path: %s", path)
            continue
        results.append((path, old_sha, new_sha))
    return results


def unique_ordered(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def is_entry_file(path: str) -> bool:
    """Check if a path looks like an executable entry point or script."""
    if SCRIPT_DIR_PATTERNS.search(path):
        return True
    return any(p.search(path) for p in ENTRY_FILE_PATTERNS)


def get_new_files(submodule_dir: Path, old_sha: str, new_sha: str) -> list[str]:
    """Get files that were added (not present in old, present in new)."""
    output = run_no_fail(
        ["git", "-C", str(submodule_dir), "diff", "--diff-filter=A", "--name-only", old_sha, new_sha]
    )
    return [line for line in output.splitlines() if line]


def get_renamed_files(submodule_dir: Path, old_sha: str, new_sha: str) -> list[tuple[str, str]]:
    """Get renamed files as (old_name, new_name) pairs."""
    output = run_no_fail(
        ["git", "-C", str(submodule_dir), "diff", "--diff-filter=R", "--name-status", "-M50%", old_sha, new_sha]
    )
    pairs: list[tuple[str, str]] = []
    for line in output.splitlines():
        parts = line.split("\t")
        if len(parts) >= 3 and parts[0].startswith("R"):
            pairs.append((parts[1], parts[2]))
    return pairs


def get_numstat(submodule_dir: Path, old_sha: str, new_sha: str) -> dict[str, tuple[int, int]]:
    """Get per-file added/deleted line counts."""
    output = run_no_fail(
        ["git", "-C", str(submodule_dir), "diff", "--numstat", old_sha, new_sha]
    )
    stats: dict[str, tuple[int, int]] = {}
    for line in output.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        added_str, deleted_str, path = parts[0], parts[1], parts[2]
        try:
            added = int(added_str) if added_str != "-" else 0
            deleted = int(deleted_str) if deleted_str != "-" else 0
        except ValueError:
            continue
        stats[path] = (added, deleted)
    return stats


def get_touch_counts(submodule_dir: Path, old_sha: str, new_sha: str) -> dict[str, int]:
    """Count how many commits touched each file in the range."""
    output = run_no_fail(
        ["git", "-C", str(submodule_dir), "log", "--format=", "--name-only", f"{old_sha}..{new_sha}"]
    )
    counts: dict[str, int] = {}
    for line in output.splitlines():
        line = line.strip()
        if line:
            counts[line] = counts.get(line, 0) + 1
    return counts


def get_executable_files(submodule_dir: Path, old_sha: str, new_sha: str) -> set[str]:
    """Detect files that gained executable permission or have shebang."""
    # Check mode changes from git diff --raw
    output = run_no_fail(
        ["git", "-C", str(submodule_dir), "diff", "--raw", old_sha, new_sha]
    )
    executables: set[str] = set()
    for line in output.splitlines():
        if "\t" not in line:
            continue
        meta, path = line.split("\t", 1)
        parts = meta.split()
        if len(parts) >= 2:
            new_mode = parts[1]
            if new_mode.endswith("755"):
                executables.add(path)
    return executables


def compute_deep_read_candidates(evidence: VendorEvidence) -> list[str]:
    """Rank files by coverage priority for deep reading.

    Order: new paths > renamed destinations > executable/entry files >
    largest churn > repeatedly touched. Deduplicate and cap at MAX_DEEP_READ_CANDIDATES.
    """
    candidates: list[str] = []
    seen: set[str] = set()

    def add(path: str) -> None:
        if path not in seen and len(candidates) < MAX_DEEP_READ_CANDIDATES:
            seen.add(path)
            candidates.append(path)

    # 1. New paths (highest priority — things that didn't exist before)
    for p in evidence.new_paths:
        add(p)

    # 2. Renamed destinations (conceptual reframing signals)
    for _, new_name in evidence.renamed_paths:
        add(new_name)

    # 3. Executable / entry-point files
    for p in evidence.executable_or_entry_files:
        add(p)

    # 4. Largest churn files (by lines changed)
    for fs in evidence.largest_churn_files:
        add(fs.path)

    # 5. Repeatedly touched files (by commit count)
    for path, _ in evidence.repeatedly_touched_files:
        add(path)

    return candidates


def build_evidence(path: str, old_sha: str, new_sha: str, repo_root: Path) -> VendorEvidence:
    submodule_dir = repo_root / path
    if not submodule_dir.exists():
        raise FileNotFoundError(f"Submodule directory does not exist: {submodule_dir}")

    # Commits
    commits = run(
        ["git", "-C", str(submodule_dir), "log", "--reverse", "--format=%h %s", f"{old_sha}..{new_sha}"]
    ).splitlines()

    # All changed files
    all_changed = [
        line for line in run(
            ["git", "-C", str(submodule_dir), "diff", "--name-only", old_sha, new_sha]
        ).splitlines() if line
    ]

    # Evidence buckets
    new_paths = get_new_files(submodule_dir, old_sha, new_sha)
    renamed_paths = get_renamed_files(submodule_dir, old_sha, new_sha)
    numstat = get_numstat(submodule_dir, old_sha, new_sha)
    touch_counts = get_touch_counts(submodule_dir, old_sha, new_sha)
    executable_modes = get_executable_files(submodule_dir, old_sha, new_sha)

    # Build FileStats for churn ranking
    file_stats: list[FileStats] = []
    for fpath in all_changed:
        added, deleted = numstat.get(fpath, (0, 0))
        fs = FileStats(
            path=fpath,
            added=added,
            deleted=deleted,
            touch_count=touch_counts.get(fpath, 1),
            is_new=fpath in set(new_paths),
            is_executable=fpath in executable_modes,
        )
        file_stats.append(fs)

    # Sort by churn (lines added + deleted) descending
    largest_churn = sorted(file_stats, key=lambda f: f.churn, reverse=True)[:MAX_FILES_PER_BUCKET]

    # Executable or entry-point files
    exec_or_entry = unique_ordered(
        fs.path for fs in file_stats
        if fs.is_executable or is_entry_file(fs.path)
    )

    # Repeatedly touched files (touched by 2+ commits)
    repeatedly_touched = sorted(
        [(p, c) for p, c in touch_counts.items() if c >= 2],
        key=lambda x: x[1],
        reverse=True,
    )[:MAX_FILES_PER_BUCKET]

    evidence = VendorEvidence(
        path=path,
        old_sha=old_sha,
        new_sha=new_sha,
        commits=commits,
        all_changed_files=all_changed,
        new_paths=new_paths,
        renamed_paths=renamed_paths,
        largest_churn_files=largest_churn,
        executable_or_entry_files=exec_or_entry,
        repeatedly_touched_files=repeatedly_touched,
    )
    evidence.deep_read_candidates = compute_deep_read_candidates(evidence)
    return evidence


def render_report(base: str, head: str, evidences: list[VendorEvidence]) -> str:
    lines: list[str] = [
        "# Vendor Evolution Evidence Report",
        "",
        f"- Base: `{base}`",
        f"- Head: `{head}`",
        f"- Updated vendors: `{len(evidences)}`",
        "",
    ]

    for ev in evidences:
        lines.extend([
            f"## `{ev.path}`",
            "",
            f"- Range: `{ev.old_sha[:12]}..{ev.new_sha[:12]}`",
            f"- Commits: `{len(ev.commits)}`",
            f"- Changed files: `{len(ev.all_changed_files)}`",
            "",
        ])

        # Commits
        lines.extend(["### Commits", ""])
        if ev.commits:
            lines.extend(f"- {c}" for c in ev.commits)
        else:
            lines.append("- No commits found in range.")
        lines.append("")

        # Deep-Read Candidates (most important section)
        lines.extend(["### Deep-Read Candidates (Top Priority)", ""])
        if ev.deep_read_candidates:
            for i, path in enumerate(ev.deep_read_candidates, 1):
                lines.append(f"{i}. `{path}`")
        else:
            lines.append("- No deep-read candidates identified.")
        lines.append("")

        # New Paths
        lines.extend(["### Discovery Evidence: New Paths", ""])
        if ev.new_paths:
            lines.extend(f"- `{p}`" for p in ev.new_paths[:MAX_FILES_PER_BUCKET])
            if len(ev.new_paths) > MAX_FILES_PER_BUCKET:
                lines.append(f"- ... and {len(ev.new_paths) - MAX_FILES_PER_BUCKET} more")
        else:
            lines.append("- No new files added.")
        lines.append("")

        # Renamed Paths
        lines.extend(["### Discovery Evidence: Renamed Paths", ""])
        if ev.renamed_paths:
            lines.extend(f"- `{old}` → `{new}`" for old, new in ev.renamed_paths[:MAX_FILES_PER_BUCKET])
        else:
            lines.append("- No renames detected.")
        lines.append("")

        # Largest Churn Files
        lines.extend(["### Discovery Evidence: Largest Churn (by lines changed)", ""])
        if ev.largest_churn_files:
            for fs in ev.largest_churn_files[:20]:
                tag = ""
                if fs.is_new:
                    tag = " [NEW]"
                elif fs.is_executable:
                    tag = " [EXEC]"
                lines.append(f"- `{fs.path}` (+{fs.added} -{fs.deleted}){tag}")
        else:
            lines.append("- No churn data available.")
        lines.append("")

        # Executable / Entry Files
        lines.extend(["### Discovery Evidence: Executable & Entry-Point Files", ""])
        if ev.executable_or_entry_files:
            lines.extend(f"- `{p}`" for p in ev.executable_or_entry_files[:MAX_FILES_PER_BUCKET])
        else:
            lines.append("- No executable or entry-point files detected.")
        lines.append("")

        # Repeatedly Touched Files
        lines.extend(["### Discovery Evidence: Repeatedly Touched Files", ""])
        if ev.repeatedly_touched_files:
            lines.extend(
                f"- `{path}` ({count} commits)"
                for path, count in ev.repeatedly_touched_files[:20]
            )
        else:
            lines.append("- No files touched by 2+ commits.")
        lines.append("")

        # All Changed Files (compact reference)
        lines.extend(["### All Changed Files", ""])
        lines.extend(f"- `{p}`" for p in ev.all_changed_files[:50])
        if len(ev.all_changed_files) > 50:
            lines.append(f"- ... and {len(ev.all_changed_files) - 50} more files")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    args = parse_args()
    repo_root = Path.cwd()

    changed = changed_vendor_gitlinks(args.base, args.head)
    if args.vendors:
        selected = set(args.vendors)
        changed = [item for item in changed if item[0] in selected]

    if not changed:
        LOGGER.warning("No changed vendor submodules found between %s and %s", args.base, args.head)
        report = render_report(args.base, args.head, [])
    else:
        evidences = [
            build_evidence(path, old_sha, new_sha, repo_root)
            for path, old_sha, new_sha in changed
        ]
        report = render_report(args.base, args.head, evidences)

    if args.write:
        output_path = repo_root / args.write
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        LOGGER.info("Wrote report to %s", output_path)
    else:
        sys.stdout.write(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
