"""Repository analysis engine — computes high-level insights from raw git data."""

from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from repovision.core.git_utils import (
    CommitInfo,
    FileStat,
    get_author_stats,
    get_commit_count,
    get_commits,
    get_contributor_count,
    get_current_branch,
    get_file_stats,
    get_repo_age,
    get_repo_size_mb,
    get_branches,
)


class RepositoryAnalysis:
    """Comprehensive analysis of a git repository.

    This is the main data object that feeds both the terminal dashboard
    and the HTML report. It aggregates all statistics into one place.
    """

    def __init__(self, repo_root: Path, max_commits: int = 500):
        self.repo_root = repo_root
        self.repo_name = repo_root.name
        self.analyzed_at = datetime.now(timezone.utc)

        # Basic info
        self.current_branch = get_current_branch(repo_root)
        self.total_commits = get_commit_count(repo_root)
        self.contributor_count = get_contributor_count(repo_root)
        self.repo_size_mb = get_repo_size_mb(repo_root)
        self.branches = get_branches(repo_root)

        # Time-based info
        self.first_commit, self.last_commit = get_repo_age(repo_root)
        if self.first_commit and self.last_commit:
            self.age_days = (self.last_commit - self.first_commit).days
        else:
            self.age_days = 0

        # Detailed data
        self.commits = get_commits(repo_root, max_commits=max_commits)
        self.commits_analyzed = len(self.commits)
        self.file_stats = get_file_stats(repo_root, max_commits=max_commits)
        self.author_stats = get_author_stats(repo_root, max_commits=max_commits)

        # Computed insights
        self.commit_frequency = self._compute_commit_frequency()
        self.hourly_activity = self._compute_hourly_activity()
        self.weekly_activity = self._compute_weekly_activity()
        self.top_files = self._compute_top_files(10)
        self.top_authors = self.author_stats[:10]
        self.hotspots = self._compute_hotspots(10)
        self.recent_activity = self._compute_recent_activity(14)
        self.health_score = self._compute_health_score()
        self.languages = self._detect_languages()

    def _compute_commit_frequency(self) -> dict[str, int]:
        """Compute commits per month for the last 12 months."""
        if not self.commits:
            return {}

        now = datetime.now(timezone.utc)
        months = {}
        for i in range(11, -1, -1):
            key = (now - timedelta(days=30 * i)).strftime("%Y-%m")
            months[key] = 0

        for commit in self.commits:
            key = commit.date.strftime("%Y-%m")
            if key in months:
                months[key] += 1

        return months

    def _compute_hourly_activity(self) -> dict[int, int]:
        """Compute commit count by hour of day (0-23)."""
        hours: dict[int, int] = {h: 0 for h in range(24)}
        for commit in self.commits:
            hours[commit.date.hour] += 1
        return hours

    def _compute_weekly_activity(self) -> dict[str, int]:
        """Compute commit count by day of week."""
        days = {d: 0 for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}
        day_map = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
        for commit in self.commits:
            day_name = day_map[commit.date.weekday()]
            days[day_name] += 1
        return days

    def _compute_top_files(self, n: int = 10) -> list[dict]:
        """Compute the top N most-changed files."""
        sorted_files = sorted(
            self.file_stats.values(), key=lambda f: f.churn, reverse=True
        )
        result = []
        for f in sorted_files[:n]:
            result.append({
                "path": f.path,
                "commits": f.total_commits,
                "insertions": f.total_insertions,
                "deletions": f.total_deletions,
                "churn": f.churn,
                "authors": len(f.authors),
                "lines": f.lines,
            })
        return result

    def _compute_hotspots(self, n: int = 10) -> list[dict]:
        """Compute code hotspots — files with high churn and recent changes.

        Hotspots are files that change frequently AND have been changed recently,
        weighted by a combined score.
        """
        if not self.file_stats:
            return []

        now = datetime.now(timezone.utc)
        scored_files = []

        for f in self.file_stats.values():
            # Recency score: 1.0 if changed today, decaying to 0 over 90 days
            recency = 0.0
            if f.last_modified:
                days_since = (now - f.last_modified).days
                recency = max(0, 1.0 - (days_since / 90))

            # Normalize churn relative to max churn
            max_churn = max(fs.churn for fs in self.file_stats.values()) or 1
            churn_norm = f.churn / max_churn

            # Combined hotspot score
            score = (0.6 * churn_norm) + (0.4 * recency)

            scored_files.append({
                "path": f.path,
                "churn": f.churn,
                "commits": f.total_commits,
                "authors": len(f.authors),
                "last_modified": f.last_modified,
                "score": round(score * 100, 1),
            })

        scored_files.sort(key=lambda x: x["score"], reverse=True)
        return scored_files[:n]

    def _compute_recent_activity(self, days: int = 14) -> dict[str, int]:
        """Compute commits per day for the last N days."""
        result = {}
        now = datetime.now(timezone.utc)
        for i in range(days - 1, -1, -1):
            date_key = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            result[date_key] = 0

        cutoff = now - timedelta(days=days)
        for commit in self.commits:
            if commit.date >= cutoff:
                date_key = commit.date.strftime("%Y-%m-%d")
                if date_key in result:
                    result[date_key] += 1

        return result

    def _compute_health_score(self) -> dict:
        """Compute a composite repository health score (0-100).

        Factors:
        - Recent activity (last 30 days)
        - Contributor diversity
        - Commit frequency
        - File churn distribution (is churn concentrated or spread?)
        """
        score = 0
        details = {}

        # 1. Recent activity (30 points)
        if self.commits:
            now = datetime.now(timezone.utc)
            cutoff = now - timedelta(days=30)
            recent = sum(1 for c in self.commits if c.date >= cutoff)
            recent_score = min(30, recent * 3)  # 10 recent commits = full score
            details["Recent Activity"] = f"{recent_score}/30 ({recent} commits in last 30 days)"
            score += recent_score

        # 2. Contributor diversity (25 points)
        contributor_score = min(25, self.contributor_count * 5)  # 5 contributors = full
        details["Contributor Diversity"] = f"{contributor_score}/25 ({self.contributor_count} contributors)"
        score += contributor_score

        # 3. Commit consistency (25 points)
        if self.commits:
            commit_count = len(self.commits)
            if self.age_days > 0:
                avg_per_week = (commit_count / self.age_days) * 7
                consistency_score = min(25, int(avg_per_week * 5))  # 5/week = full
            else:
                consistency_score = 25
            details["Commit Consistency"] = f"{consistency_score}/25"
            score += consistency_score

        # 4. Churn distribution (20 points)
        if self.file_stats:
            churns = sorted([f.churn for f in self.file_stats.values()], reverse=True)
            if len(churns) > 1:
                top_3_pct = sum(churns[:3]) / sum(churns) * 100 if sum(churns) > 0 else 100
                # Lower concentration = healthier (more spread out)
                if top_3_pct < 30:
                    dist_score = 20
                elif top_3_pct < 50:
                    dist_score = 15
                elif top_3_pct < 70:
                    dist_score = 10
                else:
                    dist_score = 5
            else:
                dist_score = 10
            details["Churn Distribution"] = f"{dist_score}/20"
            score += dist_score

        return {
            "overall": min(100, score),
            "grade": self._score_to_grade(score),
            "details": details,
        }

    def _score_to_grade(self, score: int) -> str:
        """Convert a numeric score to a letter grade."""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"

    def _detect_languages(self) -> list[dict[str, object]]:
        """Detect programming languages used in the repository."""
        extensions = Counter()
        for filepath in self.file_stats:
            ext = Path(filepath).suffix.lower()
            if ext:
                extensions[ext] += self.file_stats[filepath].lines

        lang_map = {
            ".py": ("Python", "#3572A5"),
            ".js": ("JavaScript", "#f1e05a"),
            ".ts": ("TypeScript", "#3178c6"),
            ".tsx": ("TypeScript React", "#3178c6"),
            ".jsx": ("JavaScript React", "#f1e05a"),
            ".rs": ("Rust", "#dea584"),
            ".go": ("Go", "#00ADD8"),
            ".java": ("Java", "#b07219"),
            ".cpp": ("C++", "#f34b7d"),
            ".c": ("C", "#555555"),
            ".h": ("C/C++ Header", "#555555"),
            ".rb": ("Ruby", "#701516"),
            ".php": ("PHP", "#4F5D95"),
            ".swift": ("Swift", "#F05138"),
            ".kt": ("Kotlin", "#A97BFF"),
            ".scala": ("Scala", "#c22d40"),
            ".cs": ("C#", "#178600"),
            ".css": ("CSS", "#563d7c"),
            ".scss": ("SCSS", "#c6538c"),
            ".html": ("HTML", "#e34c26"),
            ".vue": ("Vue", "#41b883"),
            ".svelte": ("Svelte", "#ff3e00"),
            ".md": ("Markdown", "#083fa1"),
            ".json": ("JSON", "#292929"),
            ".yaml": ("YAML", "#cb171e"),
            ".yml": ("YAML", "#cb171e"),
            ".toml": ("TOML", "#9c4221"),
            ".sh": ("Shell", "#89e051"),
            ".bash": ("Bash", "#89e051"),
            ".sql": ("SQL", "#e38c00"),
            ".r": ("R", "#198CE7"),
            ".dart": ("Dart", "#00B4AB"),
            ".lua": ("Lua", "#000080"),
            ".zig": ("Zig", "#ec915c"),
        }

        result = []
        for ext, lines in extensions.most_common(8):
            lang_name, color = lang_map.get(ext, (ext.lstrip(".").upper() or "Other", "#8b8b8b"))
            result.append({
                "name": lang_name,
                "extension": ext,
                "lines": lines,
                "color": color,
            })

        return result


def analyze_repo(path: Optional[Path] = None, max_commits: int = 500) -> RepositoryAnalysis:
    """Run a full analysis on a git repository.

    Args:
        path: Path to repository. Defaults to current working directory.
        max_commits: Maximum commits to analyze.

    Returns:
        A fully populated RepositoryAnalysis object.

    Raises:
        RuntimeError: If not inside a git repository.
    """
    from repovision.core.git_utils import find_git_root, is_git_repo

    if not is_git_repo(path):
        raise RuntimeError(
            "Not a git repository. Please run this command inside a git repository "
            "or specify a path to one with: repovision --path /path/to/repo"
        )

    repo_root = find_git_root(path)
    if repo_root is None:
        raise RuntimeError("Could not find git repository root.")

    return RepositoryAnalysis(repo_root, max_commits=max_commits)
