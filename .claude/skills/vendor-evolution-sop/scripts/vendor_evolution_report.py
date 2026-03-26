#!/usr/bin/env python3
"""Generate a structured markdown report from vendor submodule diffs."""

from __future__ import annotations

import argparse
import logging
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


LOGGER = logging.getLogger("vendor_evolution_report")
WORKFLOW_PATTERNS = [
    re.compile(r"(^|/)(skills?|commands|agents|hooks|plugins?|workflows?|templates?)(/|$)"),
    re.compile(r"(^|/)(SKILL\.md|plugin\.json|marketplace\.json)$"),
]


@dataclass
class VendorDelta:
    path: str
    old_sha: str
    new_sha: str
    commits: list[str]
    changed_files: list[str]
    workflow_files: list[str]


def run(cmd: list[str], cwd: Path | None = None) -> str:
    LOGGER.debug("Running command: %s", " ".join(cmd))
    try:
        completed = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        LOGGER.error("Command failed: %s", " ".join(cmd))
        if exc.stderr:
            LOGGER.error(exc.stderr.strip())
        raise
    return completed.stdout


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a markdown report for changed vendor submodules."
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
            LOGGER.info("Skipping add/delete vendor path without commit range: %s", path)
            continue
        results.append((path, old_sha, new_sha))
    return results


def is_workflow_file(path: str) -> bool:
    return any(pattern.search(path) for pattern in WORKFLOW_PATTERNS)


def unique_ordered(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def vendor_delta(path: str, old_sha: str, new_sha: str, repo_root: Path) -> VendorDelta:
    submodule_dir = repo_root / path
    if not submodule_dir.exists():
        raise FileNotFoundError(f"Submodule directory does not exist: {submodule_dir}")

    commits = run(
        ["git", "-C", str(submodule_dir), "log", "--reverse", "--format=%h %s", f"{old_sha}..{new_sha}"]
    ).splitlines()
    changed_files = [
        line
        for line in run(
            ["git", "-C", str(submodule_dir), "diff", "--name-only", old_sha, new_sha]
        ).splitlines()
        if line
    ]
    workflow_files = unique_ordered(
        path for path in changed_files if is_workflow_file(path)
    )
    return VendorDelta(
        path=path,
        old_sha=old_sha,
        new_sha=new_sha,
        commits=commits,
        changed_files=changed_files,
        workflow_files=workflow_files,
    )


def render_report(base: str, head: str, deltas: list[VendorDelta]) -> str:
    lines: list[str] = [
        "# Vendor Evolution Report",
        "",
        f"- Base: `{base}`",
        f"- Head: `{head}`",
        f"- Updated vendors: `{len(deltas)}`",
        "",
    ]

    for delta in deltas:
        lines.extend(
            [
                f"## `{delta.path}`",
                "",
                f"- Range: `{delta.old_sha[:12]}..{delta.new_sha[:12]}`",
                f"- Commit count: `{len(delta.commits)}`",
                "",
                "### Commits",
                "",
            ]
        )
        if delta.commits:
            lines.extend(f"- {commit}" for commit in delta.commits)
        else:
            lines.append("- No commit subjects found in range.")
        lines.extend(["", "### Workflow Signals", ""])
        if delta.workflow_files:
            lines.extend(f"- `{path}`" for path in delta.workflow_files[:20])
        else:
            lines.append("- No skill/workflow signal files detected.")
        lines.extend(["", "### All Changed Files", ""])
        lines.extend(f"- `{path}`" for path in delta.changed_files[:40])
        if len(delta.changed_files) > 40:
            lines.append(f"- ... and {len(delta.changed_files) - 40} more files")
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
        deltas = [vendor_delta(path, old_sha, new_sha, repo_root) for path, old_sha, new_sha in changed]
        report = render_report(args.base, args.head, deltas)

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
