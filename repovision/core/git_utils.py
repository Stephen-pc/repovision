"""Git repository operations — the low-level interface to git data."""

import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class CommitInfo:
    """Structured representation of a single git commit."""

    hash: str
    author: str
    email: str
    date: datetime
    subject: str
    files_changed: int = 0
    insertions: int = 0
    deletions: int = 0


@dataclass
class FileStat:
    """Statistics for a single file in the repository."""

    path: str
    total_commits: int = 0
    total_insertions: int = 0
    total_deletions: int = 0
    last_modified: Optional[datetime] = None
    authors: set = field(default_factory=set)
    lines: int = 0
    churn: int = 0  # insertions + deletions

    def __post_init__(self):
        self.churn = self.total_insertions + self.total_deletions


@dataclass
class AuthorStat:
    """Statistics for a single author."""

    name: str
    email: str
    commits: int = 0
    insertions: int = 0
    deletions: int = 0
    first_commit: Optional[datetime] = None
    last_commit: Optional[datetime] = None
    files_touched: set = field(default_factory=set)
    active_days: set = field(default_factory=set)


def find_git_root(path: Optional[Path] = None) -> Optional[Path]:
    """Find the root of the current git repository.

    Args:
        path: Starting path. Defaults to current working directory.

    Returns:
        Path to the git repository root, or None if not in a repo.
    """
    start = Path(path) if path else Path.cwd()
    current = start.resolve()
    while True:
        git_dir = current / ".git"
        if git_dir.exists():
            return current
        parent = current.parent
        if parent == current:
            return None
        current = parent


def run_git(args: list[str], cwd: Optional[Path] = None) -> str:
    """Run a git command and return its stdout.

    Args:
        args: Git command arguments (without 'git' prefix).
        cwd: Working directory for the command.

    Returns:
        Command stdout as string, stripped of trailing whitespace.

    Raises:
        RuntimeError: If the git command fails.
    """
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            cwd=str(cwd) if cwd else None,
            check=True,
            timeout=30,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git command failed: {' '.join(args)}\n{e.stderr}") from e
    except FileNotFoundError:
        raise RuntimeError(
            "Git is not installed or not found in PATH. "
            "Please install git: https://git-scm.com/downloads"
        ) from None


def get_commit_count(repo_root: Path) -> int:
    """Get the total number of commits in the repository."""
    try:
        return int(run_git(["rev-list", "--count", "HEAD"], cwd=repo_root))
    except RuntimeError:
        return 0


def get_branches(repo_root: Path) -> list[str]:
    """Get list of all branch names."""
    output = run_git(
        ["branch", "-a", "--format=%(refname:short)"], cwd=repo_root
    )
    return [b for b in output.split("\n") if b and not b.startswith("origin/")]


def get_commits(
    repo_root: Path,
    max_commits: int = 500,
    since: Optional[str] = None,
    author: Optional[str] = None,
) -> list[CommitInfo]:
    """Retrieve commit history from the repository.

    Args:
        repo_root: Path to git repository root.
        max_commits: Maximum number of commits to retrieve.
        since: Date string for `--since` filter (e.g. "2024-01-01").
        author: Filter by author name or email.

    Returns:
        List of CommitInfo objects.
    """
    args = [
        "log",
        f"-{max_commits}",
        "--format=%H%x00%an%x00%ae%x00%aI%x00%s",
        "--numstat",
    ]
    if since:
        args.append(f"--since={since}")
    if author:
        args.append(f"--author={author}")

    try:
        output = run_git(args, cwd=repo_root)
    except RuntimeError:
        return []

    if not output:
        return []

    commits = []
    current = None
    lines = output.split("\n")

    for line in lines:
        if not line.strip():
            continue

        # Check if this is a commit header line (contains null bytes)
        if "\x00" in line:
            parts = line.split("\x00")
            if len(parts) >= 5:
                try:
                    date = datetime.fromisoformat(parts[3])
                except (ValueError, IndexError):
                    date = datetime.now(timezone.utc)

                current = CommitInfo(
                    hash=parts[0][:8] if parts[0] else "unknown",
                    author=parts[1] if len(parts) > 1 else "unknown",
                    email=parts[2] if len(parts) > 2 else "unknown",
                    date=date,
                    subject=parts[4] if len(parts) > 4 else "",
                )
                commits.append(current)
        elif current is not None:
            # This is a numstat line: insertions\tt deletions\tfile
            parts = line.split("\t")
            if len(parts) == 3:
                try:
                    ins = int(parts[0]) if parts[0] != "-" else 0
                    dels = int(parts[1]) if parts[1] != "-" else 0
                    current.files_changed += 1
                    current.insertions += ins
                    current.deletions += dels
                except ValueError:
                    pass

    return commits


def get_file_stats(repo_root: Path, max_commits: int = 500) -> dict[str, FileStat]:
    """Build per-file statistics from git history.

    Args:
        repo_root: Path to git repository root.
        max_commits: Number of commits to analyze.

    Returns:
        Dictionary mapping file paths to FileStat objects.
    """
    # Parse numstat data from commits
    file_stats: dict[str, FileStat] = {}

    # Use git log with specific format
    try:
        output = run_git(
            [
                "log",
                f"-{max_commits}",
                "--format=COMMIT %H%x00%an%x00%ae%x00%aI",
                "--numstat",
            ],
            cwd=repo_root,
        )
    except RuntimeError:
        return {}

    current_author = ""
    current_email = ""
    current_date: Optional[datetime] = None

    for line in output.split("\n"):
        if not line.strip():
            continue

        if line.startswith("COMMIT "):
            parts = line[7:].split("\x00", 3)
            current_author = parts[1] if len(parts) > 1 else ""
            current_email = parts[2] if len(parts) > 2 else ""
            try:
                current_date = datetime.fromisoformat(parts[3]) if len(parts) > 3 else None
            except ValueError:
                current_date = None
        elif "\t" in line:
            parts = line.split("\t")
            if len(parts) == 3:
                filepath = parts[2]
                try:
                    ins = int(parts[0]) if parts[0] != "-" else 0
                    dels = int(parts[1]) if parts[1] != "-" else 0
                except ValueError:
                    continue

                if filepath not in file_stats:
                    file_stats[filepath] = FileStat(path=filepath)

                fs = file_stats[filepath]
                fs.total_commits += 1
                fs.total_insertions += ins
                fs.total_deletions += dels
                fs.churn = fs.total_insertions + fs.total_deletions
                if current_author:
                    fs.authors.add(current_author)
                if current_date and (fs.last_modified is None or current_date > fs.last_modified):
                    fs.last_modified = current_date

    # Try to get current line counts for existing files
    for filepath in list(file_stats.keys()):
        full_path = repo_root / filepath
        if full_path.exists() and full_path.is_file():
            try:
                with open(full_path, encoding="utf-8", errors="ignore") as f:
                    file_stats[filepath].lines = sum(1 for _ in f)
            except (OSError, PermissionError):
                pass

    return file_stats


def get_author_stats(repo_root: Path, max_commits: int = 500) -> list[AuthorStat]:
    """Build per-author statistics from git history.

    Args:
        repo_root: Path to git repository root.
        max_commits: Number of commits to analyze.

    Returns:
        List of AuthorStat objects sorted by commit count (descending).
    """
    author_map: dict[str, AuthorStat] = {}

    # Get per-file data for each commit
    try:
        output = run_git(
            [
                "log",
                f"-{max_commits}",
                "--format=COMMIT %H%x00%an%x00%ae%x00%aI",
                "--numstat",
            ],
            cwd=repo_root,
        )
    except RuntimeError:
        output = ""

    current_author = ""
    current_email = ""
    current_date: Optional[datetime] = None

    for line in output.split("\n"):
        if not line.strip():
            continue

        if line.startswith("COMMIT "):
            parts = line[7:].split("\x00", 3)
            current_author = parts[1] if len(parts) > 1 else ""
            current_email = parts[2] if len(parts) > 2 else ""
            try:
                current_date = datetime.fromisoformat(parts[3]) if len(parts) > 3 else None
            except ValueError:
                current_date = None

            if current_author not in author_map:
                author_map[current_author] = AuthorStat(
                    name=current_author, email=current_email
                )

            author = author_map[current_author]
            author.commits += 1
            if current_date:
                if author.first_commit is None or current_date < author.first_commit:
                    author.first_commit = current_date
                if author.last_commit is None or current_date > author.last_commit:
                    author.last_commit = current_date
                author.active_days.add(current_date.strftime("%Y-%m-%d"))

        elif "\t" in line:
            parts = line.split("\t")
            if len(parts) == 3 and current_author in author_map:
                try:
                    ins = int(parts[0]) if parts[0] != "-" else 0
                    dels = int(parts[1]) if parts[1] != "-" else 0
                except ValueError:
                    continue
                author_map[current_author].insertions += ins
                author_map[current_author].deletions += dels
                author_map[current_author].files_touched.add(parts[2])

    return sorted(author_map.values(), key=lambda a: a.commits, reverse=True)


def get_repo_age(repo_root: Path) -> tuple[Optional[datetime], Optional[datetime]]:
    """Get the first and last commit dates in the repository.

    Returns:
        Tuple of (first_commit_date, last_commit_date).
    """
    try:
        first = run_git(
            ["log", "--reverse", "--format=%aI", "-1"], cwd=repo_root
        )
        last = run_git(
            ["log", "--format=%aI", "-1"], cwd=repo_root
        )
        first_date = datetime.fromisoformat(first) if first else None
        last_date = datetime.fromisoformat(last) if last else None
        return first_date, last_date
    except (RuntimeError, ValueError):
        return None, None


def get_current_branch(repo_root: Path) -> str:
    """Get the name of the current branch."""
    try:
        return run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_root)
    except RuntimeError:
        return "unknown"


def get_contributor_count(repo_root: Path) -> int:
    """Get the number of unique contributors."""
    try:
        output = run_git(
            ["shortlog", "-sne", "HEAD"], cwd=repo_root
        )
        return len([l for l in output.split("\n") if l.strip()])
    except RuntimeError:
        return 0


def get_repo_size_mb(repo_root: Path) -> float:
    """Estimate repository size by counting tracked files (excludes .git)."""
    # This gives a rough idea by counting file sizes (excluding .git directory)
    total = 0
    for root, dirs, files in os.walk(repo_root):
        if ".git" in dirs:
            dirs.remove(".git")
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")
        if "node_modules" in dirs:
            dirs.remove("node_modules")
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total / (1024 * 1024)


def is_git_repo(path: Optional[Path] = None) -> bool:
    """Check if a path is inside a git repository."""
    return find_git_root(path) is not None
