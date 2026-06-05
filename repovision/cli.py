"""Command-line interface for RepoVision.

Usage:
    repovision                    # Full dashboard (default)
    repovision --quick            # Compact stats view
    repovision --export report.html   # Export HTML report
    repovision --path /some/repo  # Analyze a specific repo
    repovision --commits 1000     # Analyze more commits
"""

import sys
from pathlib import Path
from typing import Optional

# Fix Unicode output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import typer
from rich.console import Console

from repovision import __version__
from repovision.core.analyzer import analyze_repo
from repovision.display.terminal import render_dashboard, render_quick_stats
from repovision.display.html_report import export_report

app = typer.Typer(
    name="repovision",
    help="🔭 Beautiful git repository analytics at your fingertips.",
    add_completion=False,
    no_args_is_help=False,
)

console = Console()


def version_callback(value: bool):
    if value:
        console.print(f"[bold]RepoVision[/] v{__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        "-p",
        help="Path to git repository (defaults to current directory).",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
    export: Optional[Path] = typer.Option(
        None,
        "--export",
        "-e",
        help="Export an interactive HTML report to the specified file.",
    ),
    quick: bool = typer.Option(
        False,
        "--quick",
        "-q",
        help="Show compact single-line stats instead of the full dashboard.",
    ),
    commits: int = typer.Option(
        500,
        "--commits",
        "-c",
        help="Number of commits to analyze (default: 500).",
        min=10,
        max=10000,
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
):
    """🔭 RepoVision — Beautiful git repository analytics at your fingertips.

    Run without options to see a beautiful terminal dashboard with
    repository statistics, contributor insights, code hotspots, and more.

    Examples:
        repovision                          # Dashboard for current repo
        repovision --quick                  # Quick stats
        repovision --export report.html     # Save HTML report
        repovision -p ~/projects/my-repo    # Analyze another repo
        repovision -c 2000                  # Analyze last 2000 commits
    """
    # Determine which repo to analyze
    target = path or Path.cwd()

    try:
        with console.status("[bold]Analyzing repository...[/]", spinner="dots"):
            analysis = analyze_repo(target, max_commits=commits)
    except RuntimeError as e:
        console.print(f"[bold red]Error:[/] {e}")
        raise typer.Exit(code=1)

    # Export HTML if requested
    if export:
        try:
            output_path = export.resolve()
            export_report(analysis, output_path)
            console.print(f"[bold green]✓[/] Report exported to [bold]{output_path}[/]")
        except OSError as e:
            console.print(f"[bold red]Error writing report:[/] {e}")
            raise typer.Exit(code=1)

    # Display results
    if not export or not quick:
        console.print()  # spacer

    if quick:
        render_quick_stats(analysis)
    elif export:
        # When only exporting, show a quick summary
        render_quick_stats(analysis)
    else:
        render_dashboard(analysis)

    console.print()  # trailing newline


@app.command(name="export")
def export_command(
    output: Path = typer.Argument(
        ...,
        help="Output file path for the HTML report (e.g., report.html).",
    ),
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        "-p",
        help="Path to git repository (defaults to current directory).",
        exists=True,
    ),
    commits: int = typer.Option(
        500,
        "--commits",
        "-c",
        help="Number of commits to analyze.",
        min=10,
        max=10000,
    ),
):
    """Export an interactive HTML report of the repository analysis.

    The report includes interactive charts, key metrics, contributor
    breakdowns, hotspot analysis, and language detection — all in a
    beautiful dark-themed, self-contained HTML file.
    """
    target = path or Path.cwd()

    try:
        with console.status("[bold]Building report...[/]", spinner="dots"):
            analysis = analyze_repo(target, max_commits=commits)
            output_path = output.resolve()
            export_report(analysis, output_path)
    except RuntimeError as e:
        console.print(f"[bold red]Error:[/] {e}")
        raise typer.Exit(code=1)
    except OSError as e:
        console.print(f"[bold red]Error writing report:[/] {e}")
        raise typer.Exit(code=1)

    console.print(f"[bold green]✓[/] Report exported to [bold]{output_path}[/]")
    console.print(f"  Open with: [dim]{output_path.as_uri()}[/]")


@app.command(name="quick")
def quick_command(
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        "-p",
        help="Path to git repository (defaults to current directory).",
        exists=True,
    ),
):
    """Show a compact, one-line summary of the repository."""
    target = path or Path.cwd()

    try:
        with console.status("[bold]Analyzing...[/]", spinner="dots"):
            analysis = analyze_repo(target)
    except RuntimeError as e:
        console.print(f"[bold red]Error:[/] {e}")
        raise typer.Exit(code=1)

    render_quick_stats(analysis)


@app.command(name="hotspots")
def hotspots_command(
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        "-p",
        help="Path to git repository (defaults to current directory).",
        exists=True,
    ),
    top: int = typer.Option(
        10,
        "--top",
        "-n",
        help="Number of hotspots to show.",
        min=1,
        max=50,
    ),
):
    """Show code hotspots — files that change frequently."""
    target = path or Path.cwd()

    try:
        with console.status("[bold]Finding hotspots...[/]", spinner="dots"):
            analysis = analyze_repo(target)
    except RuntimeError as e:
        console.print(f"[bold red]Error:[/] {e}")
        raise typer.Exit(code=1)

    from rich.table import Table
    from rich import box

    table = Table(title=f"🔥 Code Hotspots — {analysis.repo_name}", box=box.SIMPLE)
    table.add_column("File", style="bright_white")
    table.add_column("Churn", justify="right", style="yellow")
    table.add_column("Score", justify="right", style="red")
    table.add_column("Authors", justify="right")
    table.add_column("Last Modified", style="dim")

    for h in analysis.hotspots[:top]:
        lm = h["last_modified"].strftime("%Y-%m-%d") if h["last_modified"] else "N/A"
        table.add_row(
            h["path"],
            str(h["churn"]),
            str(h["score"]),
            str(h["authors"]),
            lm,
        )

    console.print(table)


@app.command(name="contributors")
def contributors_command(
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        "-p",
        help="Path to git repository (defaults to current directory).",
        exists=True,
    ),
    top: int = typer.Option(
        10,
        "--top",
        "-n",
        help="Number of contributors to show.",
        min=1,
        max=50,
    ),
):
    """Show contributor statistics."""
    target = path or Path.cwd()

    try:
        with console.status("[bold]Analyzing contributors...[/]", spinner="dots"):
            analysis = analyze_repo(target)
    except RuntimeError as e:
        console.print(f"[bold red]Error:[/] {e}")
        raise typer.Exit(code=1)

    from rich.table import Table
    from rich import box

    table = Table(title=f"👥 Contributors — {analysis.repo_name}", box=box.SIMPLE)
    table.add_column("Author", style="bright_white")
    table.add_column("Commits", justify="right", style="green")
    table.add_column("+Insertions", justify="right", style="blue")
    table.add_column("-Deletions", justify="right", style="red")
    table.add_column("Files", justify="right")
    table.add_column("Active Days", justify="right")

    for author in analysis.top_authors[:top]:
        table.add_row(
            author.name[:30],
            str(author.commits),
            f"+{author.insertions}",
            f"-{author.deletions}",
            str(len(author.files_touched)),
            str(len(author.active_days)),
        )

    console.print(table)


def main_entry():
    """Entry point for console_scripts."""
    app()


if __name__ == "__main__":
    main_entry()
