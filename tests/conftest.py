"""Shared test fixtures for RepoVision."""

import subprocess
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_git_repo():
    """Create a temporary git repository with some commit history.

    Creates:
        - 3 files with initial commits
        - 2 modifications to file_0.py
        - Total: 5 commits by "Test User"
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)

        # Initialize git repo
        subprocess.run(
            ["git", "init", "-q"], cwd=repo_path, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=repo_path, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=repo_path, check=True, capture_output=True,
        )

        # Create a few files with commits
        for i in range(3):
            file_path = repo_path / f"file_{i}.py"
            lines = [f"# File {i}", "print('hello')", ""]
            # file_0 has more lines to create interesting stats
            if i == 0:
                lines.extend(["def foo():", "    return 42", ""])
            file_path.write_text("\n".join(lines))
            subprocess.run(
                ["git", "add", file_path.name],
                cwd=repo_path, check=True, capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-q", "-m", f"Commit {i}: add file_{i}.py"],
                cwd=repo_path, check=True, capture_output=True,
            )

        # Modify file_0 a few times to create churn
        for i in range(2):
            file_0 = repo_path / "file_0.py"
            current = file_0.read_text()
            file_0.write_text(current + f"\n# Modification {i}\n")
            subprocess.run(
                ["git", "add", "file_0.py"],
                cwd=repo_path, check=True, capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-q", "-m", f"Commit {3+i}: modify file_0"],
                cwd=repo_path, check=True, capture_output=True,
            )

        yield repo_path
