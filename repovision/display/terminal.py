"""Beautiful terminal dashboard rendering using Rich."""

from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.columns import Columns
from rich.progress_bar import ProgressBar
from rich.align import Align
from rich import box

from repovision.core.analyzer import RepositoryAnalysis

console = Console()


# ── Color palette ──────────────────────────────────────────────────────────

ACCENT = "#6C5CE7"       # Purple
SUCCESS = "#00B894"      # Green
WARNING = "#FDCB6E"      # Yellow
DANGER = "#E17055"       # Coral
INFO = "#74B9FF"         # Blue
DIM = "#636E72"          # Gray
BG = "#2D3436"           # Dark


def bar_chart(
    data: dict[str, int],
    width: int = 40,
    max_val: Optional[int] = None,
    color: str = ACCENT,
) -> str:
    """Render a simple horizontal bar chart as text.

    Args:
        data: Mapping of labels to values.
        width: Maximum bar width in characters.
        max_val: Maximum value for scaling (auto-detected if None).
        color: Rich color for the bars.

    Returns:
        String with bar chart (may contain Rich markup).
    """
    if not data:
        return "No data"

    if max_val is None:
        max_val = max(data.values()) or 1

    lines = []
    for label, value in data.items():
        bar_len = int((value / max_val) * width) if max_val > 0 else 0
        bar = "█" * bar_len
        lines.append(f"  {label:>5}  [{color}]{bar}[/] {value}")

    return "\n".join(lines)


def render_overview(analysis: RepositoryAnalysis) -> Panel:
    """Render the overview panel with key metrics."""
    health = analysis.health_score
    grade_color = SUCCESS if health["overall"] >= 70 else (WARNING if health["overall"] >= 50 else DANGER)

    # Format the repo age
    if analysis.age_days > 365:
        age_str = f"{analysis.age_days / 365:.1f} years"
    elif analysis.age_days > 30:
        age_str = f"{analysis.age_days / 30:.1f} months"
    else:
        age_str = f"{analysis.age_days} days"

    content = f"""
[bright_white]Repository:[/] [bold]{analysis.repo_name}[/]
[bright_white]Branch:[/]      {analysis.current_branch}
[bright_white]Age:[/]         {age_str}
[bright_white]Size:[/]        {analysis.repo_size_mb:.1f} MB

[bold]━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]

[bright_white]Commits:[/]      [bold]{analysis.total_commits:,}[/] (analyzed {analysis.commits_analyzed:,})
[bright_white]Contributors:[/] [bold]{analysis.contributor_count}[/]
[bright_white]Branches:[/]     [bold]{len(analysis.branches)}[/]
[bright_white]Languages:[/]    [bold]{len(analysis.languages)}[/] detected

[bold]━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]

[bright_white]Health Score:[/]  [{grade_color}]{health['overall']}/100 — {health['grade']}[/]
"""
    return Panel(
        content.strip(),
        title="[bold]📊 Repository Overview[/]",
        border_style=ACCENT,
        padding=(1, 2),
    )


def render_contributors(analysis: RepositoryAnalysis) -> Panel:
    """Render the top contributors panel."""
    if not analysis.top_authors:
        return Panel("No contributor data", title="[bold]👥 Top Contributors[/]", border_style=INFO)

    table = Table(show_header=True, header_style=f"bold {INFO}", box=box.SIMPLE, padding=(0, 1))
    table.add_column("Author", style="bright_white", width=20)
    table.add_column("Commits", justify="right", style=SUCCESS)
    table.add_column("Insertions", justify="right", style=INFO)
    table.add_column("Deletions", justify="right", style=DANGER)
    table.add_column("Files", justify="right", style=DIM)

    for author in analysis.top_authors[:8]:
        table.add_row(
            author.name[:20],
            str(author.commits),
            f"+{author.insertions}",
            f"-{author.deletions}",
            str(len(author.files_touched)),
        )

    return Panel(
        table,
        title="[bold]👥 Top Contributors[/]",
        border_style=INFO,
        padding=(0, 1),
    )


def render_hotspots(analysis: RepositoryAnalysis) -> Panel:
    """Render the code hotspots panel."""
    if not analysis.hotspots:
        return Panel("No file data", title="[bold]🔥 Hotspots[/]", border_style=DANGER)

    table = Table(show_header=True, header_style=f"bold {DANGER}", box=box.SIMPLE, padding=(0, 1))
    table.add_column("File", style="bright_white", width=30)
    table.add_column("Churn", justify="right", style=WARNING)
    table.add_column("Score", justify="right", style=DANGER)
    table.add_column("Authors", justify="right", style=DIM)

    for h in analysis.hotspots[:8]:
        # Truncate path
        path = h["path"]
        if len(path) > 28:
            path = "…" + path[-27:]

        score_color = DANGER if h["score"] > 50 else (WARNING if h["score"] > 25 else DIM)
        table.add_row(
            path,
            str(h["churn"]),
            f"[{score_color}]{h['score']}[/]",
            str(h["authors"]),
        )

    return Panel(
        table,
        title="[bold]🔥 Code Hotspots[/]",
        border_style=DANGER,
        padding=(0, 1),
    )


def render_activity_chart(analysis: RepositoryAnalysis) -> Panel:
    """Render commit activity visualization."""
    # Weekly activity bar chart
    weekly_chart = bar_chart(analysis.weekly_activity, width=35, color=SUCCESS)

    # Hourly activity as a heatmap-style bar
    hourly = analysis.hourly_activity
    max_hourly = max(hourly.values()) or 1
    hour_bars = ""
    for h in range(24):
        val = hourly[h]
        if val == 0:
            bar = f"[{DIM}]▁[/]"
        elif val < max_hourly * 0.25:
            bar = f"[{INFO}]▂[/]"
        elif val < max_hourly * 0.5:
            bar = f"[{INFO}]▄[/]"
        elif val < max_hourly * 0.75:
            bar = f"[{SUCCESS}]▆[/]"
        else:
            bar = f"[{SUCCESS}]█[/]"
        hour_bars += bar
        if h == 11:
            hour_bars += "\n           "

    content = f"""
[bright_white]By Day of Week:[/]
{weekly_chart}

[bright_white]By Hour (0-23):[/]
           {hour_bars}
"""
    return Panel(
        content.strip(),
        title="[bold]📈 Commit Activity[/]",
        border_style=SUCCESS,
        padding=(1, 2),
    )


def render_recent_activity(analysis: RepositoryAnalysis) -> Panel:
    """Render recent commit activity sparkline."""
    recent = analysis.recent_activity
    if not recent:
        return Panel("No data", title="[bold]📅 Recent Activity (14 days)[/]", border_style=INFO)

    max_val = max(recent.values()) or 1

    # Build a sparkline
    spark = ""
    for date, count in recent.items():
        if count == 0:
            spark += f"[{DIM}]▁[/]"
        elif count <= max_val * 0.25:
            spark += f"[{INFO}]▂[/]"
        elif count <= max_val * 0.5:
            spark += f"[{INFO}]▅[/]"
        elif count <= max_val * 0.75:
            spark += f"[{SUCCESS}]▇[/]"
        else:
            spark += f"[{SUCCESS}]█[/]"

    total_recent = sum(recent.values())
    content = f"""
[bright_white]Last 14 days:[/] [bold]{total_recent}[/] commits

{spark}

[dim]Each bar = 1 day (oldest → newest)[/]
"""
    return Panel(
        content.strip(),
        title="[bold]📅 Recent Activity[/]",
        border_style=INFO,
        padding=(1, 2),
    )


def render_languages(analysis: RepositoryAnalysis) -> Panel:
    """Render language breakdown."""
    if not analysis.languages:
        return Panel("No language data", title="[bold]🔤 Languages[/]", border_style=WARNING)

    total_lines = sum(lang["lines"] for lang in analysis.languages)
    if total_lines == 0:
        return Panel("No code lines detected", title="[bold]🔤 Languages[/]", border_style=WARNING)

    content = ""
    for lang in analysis.languages:
        pct = (lang["lines"] / total_lines) * 100
        bar_len = int(pct / 2)  # 50 chars max
        bar = "█" * bar_len
        color = str(lang["color"]) if lang["color"].startswith("#") else "#8b8b8b"
        content += f"  [{color}]{bar}[/] {lang['name']}: {pct:.1f}%\n"

    return Panel(
        content.strip(),
        title="[bold]🔤 Languages[/]",
        border_style=WARNING,
        padding=(1, 2),
    )


def render_health_details(analysis: RepositoryAnalysis) -> Panel:
    """Render health score breakdown."""
    details = analysis.health_score["details"]
    content = "\n".join(f"  • {key}: {value}" for key, value in details.items())

    return Panel(
        content,
        title="[bold]🏥 Health Breakdown[/]",
        border_style=ACCENT,
        padding=(1, 2),
    )


def render_dashboard(analysis: RepositoryAnalysis):
    """Render the complete RepoVision terminal dashboard.

    This is the main entry point for terminal output. It arranges all
    panels into a visually appealing layout.

    Args:
        analysis: A fully populated RepositoryAnalysis object.
    """
    # Header
    header = Panel(
        Align.center(
            f"\n[bold bright_white]🔭 RepoVision[/]  •  {analysis.repo_name}\n"
            f"[dim]Analyzed at {analysis.analyzed_at.strftime('%Y-%m-%d %H:%M')}[/]\n",
            vertical="middle",
        ),
        border_style=ACCENT,
        box=box.DOUBLE,
    )

    console.print(header)

    # Row 1: Overview + Health
    console.print(Columns([
        render_overview(analysis),
        render_health_details(analysis),
    ]))

    # Row 2: Activity chart + Recent activity
    console.print(Columns([
        render_activity_chart(analysis),
        render_recent_activity(analysis),
    ]))

    # Row 3: Hotspots + Contributors
    console.print(Columns([
        render_hotspots(analysis),
        render_contributors(analysis),
    ]))

    # Row 4: Languages
    console.print(render_languages(analysis))

    # Footer
    console.print(
        Panel(
            Align.center(
                f"[dim]💡 Tip: Run[/] [bold]repovision --export report.html[/] [dim]to save an interactive HTML report[/]",
                vertical="middle",
            ),
            border_style=DIM,
            padding=(0, 1),
        )
    )


def render_quick_stats(analysis: RepositoryAnalysis):
    """Render a compact, single-line-friendly stats view.

    Args:
        analysis: A fully populated RepositoryAnalysis object.
    """
    health = analysis.health_score
    console.print(
        f"[bold]{analysis.repo_name}[/]  "
        f"📦 {analysis.total_commits:,} commits  "
        f"👥 {analysis.contributor_count} contributors  "
        f"🏥 [{SUCCESS if health['overall'] >= 70 else WARNING}]{health['overall']}/100[/]  "
        f"🔥 {len(analysis.hotspots)} hotspots"
    )
