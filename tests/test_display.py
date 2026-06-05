"""Tests for rendering modules."""

from repovision.core.analyzer import RepositoryAnalysis
from repovision.display.terminal import (
    render_overview,
    render_contributors,
    render_hotspots,
    render_activity_chart,
    render_recent_activity,
    render_languages,
    render_health_details,
    render_quick_stats,
    bar_chart,
)


def test_bar_chart():
    """bar_chart should render text bars."""
    data = {"Mon": 5, "Tue": 10, "Wed": 3}
    result = bar_chart(data, width=20)
    assert "Mon" in result
    assert "Tue" in result
    assert "Wed" in result


def test_bar_chart_empty():
    """bar_chart with empty data should not crash."""
    result = bar_chart({})
    assert "No data" in result


def test_render_overview(temp_git_repo):
    """render_overview should return a Rich Panel."""
    analysis = RepositoryAnalysis(temp_git_repo, max_commits=10)
    panel = render_overview(analysis)
    assert panel is not None
    assert hasattr(panel, "renderable")


def test_render_contributors(temp_git_repo):
    """render_contributors should return a Rich Panel."""
    analysis = RepositoryAnalysis(temp_git_repo, max_commits=10)
    panel = render_contributors(analysis)
    assert panel is not None


def test_render_hotspots(temp_git_repo):
    """render_hotspots should return a Rich Panel."""
    analysis = RepositoryAnalysis(temp_git_repo, max_commits=10)
    panel = render_hotspots(analysis)
    assert panel is not None


def test_render_activity_chart(temp_git_repo):
    """render_activity_chart should return a Rich Panel."""
    analysis = RepositoryAnalysis(temp_git_repo, max_commits=10)
    panel = render_activity_chart(analysis)
    assert panel is not None


def test_render_recent_activity(temp_git_repo):
    """render_recent_activity should return a Rich Panel."""
    analysis = RepositoryAnalysis(temp_git_repo, max_commits=10)
    panel = render_recent_activity(analysis)
    assert panel is not None


def test_render_languages(temp_git_repo):
    """render_languages should return a Rich Panel."""
    analysis = RepositoryAnalysis(temp_git_repo, max_commits=10)
    panel = render_languages(analysis)
    assert panel is not None


def test_render_health_details(temp_git_repo):
    """render_health_details should return a Rich Panel."""
    analysis = RepositoryAnalysis(temp_git_repo, max_commits=10)
    panel = render_health_details(analysis)
    assert panel is not None


def test_render_quick_stats(temp_git_repo, capsys):
    """render_quick_stats should print stats without error."""
    analysis = RepositoryAnalysis(temp_git_repo, max_commits=10)
    render_quick_stats(analysis)
    captured = capsys.readouterr()
    # Should contain the repo name
    assert analysis.repo_name in captured.out
