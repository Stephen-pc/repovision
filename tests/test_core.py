"""Tests for RepoVision core modules."""

import tempfile
import subprocess
from pathlib import Path

import pytest

from repovision.core.git_utils import (
    find_git_root,
    is_git_repo,
    get_commit_count,
    get_commits,
    get_author_stats,
    get_file_stats,
    CommitInfo,
    FileStat,
    AuthorStat,
)
from repovision.core.analyzer import RepositoryAnalysis, analyze_repo


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def temp_git_repo():
    """Create a temporary git repository with some commit history."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)

        # Initialize git repo
        subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True)
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
            file_path.write_text(f"# File {i}\nprint('hello')\n" * (i + 3))
            subprocess.run(["git", "add", file_path.name], cwd=repo_path, check=True, capture_output=True)
            subprocess.run(
                ["git", "commit", "-m", f"Commit {i}: add file_{i}.py"],
                cwd=repo_path, check=True, capture_output=True,
            )

        # Modify file_0 a few times
        for i in range(2):
            file_0 = repo_path / "file_0.py"
            current = file_0.read_text()
            file_0.write_text(current + f"\n# Modification {i}\n")
            subprocess.run(["git", "add", "file_0.py"], cwd=repo_path, check=True, capture_output=True)
            subprocess.run(
                ["git", "commit", "-m", f"Commit {3+i}: modify file_0"],
                cwd=repo_path, check=True, capture_output=True,
            )

        yield repo_path


# ── Git Utils Tests ─────────────────────────────────────────────────────────

class TestGitUtils:
    """Tests for git utility functions."""

    def test_find_git_root_in_repo(self, temp_git_repo):
        """find_git_root should return the repo root when inside a git repo."""
        root = find_git_root(temp_git_repo)
        assert root == temp_git_repo

    def test_find_git_root_in_subdir(self, temp_git_repo):
        """find_git_root should find the root from a subdirectory."""
        subdir = temp_git_repo / "subdir"
        subdir.mkdir()
        root = find_git_root(subdir)
        assert root == temp_git_repo

    def test_find_git_root_outside_repo(self):
        """find_git_root should return None outside a git repo."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = find_git_root(Path(tmpdir))
            assert root is None

    def test_is_git_repo_true(self, temp_git_repo):
        """is_git_repo should return True inside a git repo."""
        assert is_git_repo(temp_git_repo) is True

    def test_is_git_repo_false(self):
        """is_git_repo should return False outside a git repo."""
        with tempfile.TemporaryDirectory() as tmpdir:
            assert is_git_repo(Path(tmpdir)) is False

    def test_get_commit_count(self, temp_git_repo):
        """get_commit_count should return the correct number of commits."""
        count = get_commit_count(temp_git_repo)
        assert count == 5

    def test_get_commits(self, temp_git_repo):
        """get_commits should return CommitInfo objects with correct data."""
        commits = get_commits(temp_git_repo, max_commits=10)
        assert len(commits) == 5
        assert all(isinstance(c, CommitInfo) for c in commits)
        # Commits are in reverse chronological order
        assert commits[0].author == "Test User"
        assert commits[0].email == "test@example.com"

    def test_get_commits_limit(self, temp_git_repo):
        """get_commits should honor the max_commits parameter."""
        commits = get_commits(temp_git_repo, max_commits=2)
        assert len(commits) == 2

    def test_get_author_stats(self, temp_git_repo):
        """get_author_stats should return correct author statistics."""
        authors = get_author_stats(temp_git_repo)
        assert len(authors) == 1
        assert authors[0].name == "Test User"
        assert authors[0].commits == 5

    def test_get_file_stats(self, temp_git_repo):
        """get_file_stats should return per-file statistics."""
        stats = get_file_stats(temp_git_repo)
        assert "file_0.py" in stats
        assert stats["file_0.py"].total_commits >= 3  # created + 2 modifications
        assert isinstance(stats["file_0.py"], FileStat)


# ── Repository Analysis Tests ───────────────────────────────────────────────

class TestRepositoryAnalysis:
    """Tests for the RepositoryAnalysis class."""

    def test_basic_analysis(self, temp_git_repo):
        """RepositoryAnalysis should populate all basic fields."""
        analysis = RepositoryAnalysis(temp_git_repo, max_commits=10)
        assert analysis.total_commits == 5
        assert analysis.contributor_count == 1
        assert analysis.repo_name == temp_git_repo.name
        assert len(analysis.commits) == 5

    def test_analyze_repo_helper(self, temp_git_repo):
        """analyze_repo helper should work end-to-end."""
        analysis = analyze_repo(temp_git_repo)
        assert analysis is not None
        assert analysis.total_commits == 5

    def test_analyze_repo_not_a_repo(self):
        """analyze_repo should raise RuntimeError outside a git repo."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(RuntimeError, match="Not a git repository"):
                analyze_repo(Path(tmpdir))

    def test_health_score_range(self, temp_git_repo):
        """Health score should be between 0 and 100."""
        analysis = RepositoryAnalysis(temp_git_repo)
        score = analysis.health_score["overall"]
        assert 0 <= score <= 100

    def test_weekly_activity(self, temp_git_repo):
        """Weekly activity should have 7 days."""
        analysis = RepositoryAnalysis(temp_git_repo)
        assert len(analysis.weekly_activity) == 7

    def test_hourly_activity(self, temp_git_repo):
        """Hourly activity should have 24 hours."""
        analysis = RepositoryAnalysis(temp_git_repo)
        assert len(analysis.hourly_activity) == 24

    def test_languages_detected(self, temp_git_repo):
        """Languages should detect Python files."""
        analysis = RepositoryAnalysis(temp_git_repo)
        # We created .py files
        py_langs = [l for l in analysis.languages if l["name"] == "Python"]
        assert len(py_langs) == 1

    def test_top_files(self, temp_git_repo):
        """Top files should be sorted by churn."""
        analysis = RepositoryAnalysis(temp_git_repo)
        assert len(analysis.top_files) > 0
        # file_0.py has more churn (created + 2 mods)
        assert analysis.top_files[0]["path"] == "file_0.py"

    def test_hotspots(self, temp_git_repo):
        """Hotspots should be computed."""
        analysis = RepositoryAnalysis(temp_git_repo)
        assert len(analysis.hotspots) > 0


# ── Edge Cases ──────────────────────────────────────────────────────────────

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_repo(self):
        """Analysis of a repo with no commits should not crash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True)
            # No commits yet
            analysis = RepositoryAnalysis(repo_path)
            assert analysis.total_commits == 0
            assert len(analysis.commits) == 0

    def test_non_ascii_content(self, temp_git_repo):
        """Should handle non-ASCII file content gracefully."""
        file_path = temp_git_repo / "unicode.py"
        file_path.write_text("# 中文注释\nprint('你好世界')\n", encoding="utf-8")
        subprocess.run(["git", "add", "unicode.py"], cwd=temp_git_repo, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Add unicode file"],
            cwd=temp_git_repo, check=True, capture_output=True,
        )
        # Should not raise
        analysis = RepositoryAnalysis(temp_git_repo)
        assert "unicode.py" in analysis.file_stats
