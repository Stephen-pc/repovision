"""Tests for HTML report generation."""

import tempfile
from pathlib import Path

from repovision.core.analyzer import RepositoryAnalysis
from repovision.display.html_report import generate_html_report, export_report


def test_generate_html_report(temp_git_repo):
    """generate_html_report should produce valid HTML."""
    analysis = RepositoryAnalysis(temp_git_repo, max_commits=10)
    html = generate_html_report(analysis)

    assert "<!DOCTYPE html>" in html
    assert "RepoVision" in html
    assert "Chart.js" in html or "chart.js" in html
    assert analysis.repo_name in html


def test_export_report_writes_file(temp_git_repo):
    """export_report should write an HTML file."""
    analysis = RepositoryAnalysis(temp_git_repo, max_commits=10)

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "report.html"
        result = export_report(analysis, output_path)

        assert result == output_path
        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in content


def test_html_report_contains_key_data(temp_git_repo):
    """HTML report should contain key analysis data."""
    analysis = RepositoryAnalysis(temp_git_repo, max_commits=10)
    html = generate_html_report(analysis)

    # Should contain health score
    assert str(analysis.health_score["overall"]) in html
    # Should contain contributor count
    assert str(analysis.contributor_count) in html
    # Should contain repo name
    assert analysis.repo_name in html
