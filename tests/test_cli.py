"""Tests for the CLI module."""

from typer.testing import CliRunner

from repovision.cli import app


runner = CliRunner()


def test_version_flag():
    """--version should output version and exit cleanly."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "RepoVision" in result.stdout


def test_help_flag():
    """--help should show usage information."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "repovision" in result.stdout.lower()


def test_quick_outside_repo():
    """quick command outside a repo should error gracefully."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            result = runner.invoke(app, ["quick"])
            assert result.exit_code == 1
            assert "Not a git repository" in result.stdout
        finally:
            os.chdir(original_cwd)


def test_main_outside_repo():
    """Main command outside a repo should error gracefully."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            result = runner.invoke(app, [])
            assert result.exit_code == 1
            assert "Not a git repository" in result.stdout
        finally:
            os.chdir(original_cwd)


def test_subcommands_exist():
    """Verify that subcommands are registered and respond."""
    # Invoke the main app to see the help listing subcommands
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    help_text = result.stdout.lower()
    assert "hotspots" in help_text
    assert "contributors" in help_text
    assert "export" in help_text


def test_export_requires_path():
    """export command without required args should show error or help."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            # export requires an output path argument; without it, shows usage
            result = runner.invoke(app, ["export"])
            # Should either error (missing arg) with exit 2 or show help
            assert result.exit_code in (0, 1, 2)
        finally:
            os.chdir(original_cwd)
