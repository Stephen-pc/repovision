"""Interactive HTML report generation."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from repovision.core.analyzer import RepositoryAnalysis

# HTML template with embedded Chart.js for interactive charts
# No external dependencies needed — Chart.js loads from CDN
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RepoVision — {{ repo_name }}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        :root {
            --bg: #0d1117;
            --bg-card: #161b22;
            --border: #30363d;
            --text: #c9d1d9;
            --text-dim: #8b949e;
            --accent: #6C5CE7;
            --green: #00B894;
            --yellow: #FDCB6E;
            --red: #E17055;
            --blue: #74B9FF;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }

        .header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
            border-bottom: 1px solid var(--border);
            padding: 48px 24px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent), var(--blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }

        .header .subtitle {
            color: var(--text-dim);
            font-size: 1.1rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 32px 24px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
        }

        .card h3 {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-dim);
            margin-bottom: 16px;
        }

        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
        }

        .metric-label {
            color: var(--text-dim);
            font-size: 0.9rem;
            margin-top: 4px;
        }

        .chart-container {
            position: relative;
            height: 300px;
            margin: 16px 0;
        }

        .chart-container.tall {
            height: 400px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            text-align: left;
            padding: 10px 12px;
            border-bottom: 1px solid var(--border);
        }

        th {
            color: var(--text-dim);
            font-weight: 600;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        td {
            font-size: 0.9rem;
        }

        .badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .badge-high { background: rgba(225, 112, 85, 0.2); color: var(--red); }
        .badge-medium { background: rgba(253, 203, 110, 0.2); color: var(--yellow); }
        .badge-low { background: rgba(0, 184, 148, 0.2); color: var(--green); }

        .language-bar {
            display: flex;
            height: 12px;
            border-radius: 6px;
            overflow: hidden;
            margin: 12px 0;
        }

        .lang-legend {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 8px;
        }

        .lang-item {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.85rem;
        }

        .lang-dot {
            width: 12px;
            height: 12px;
            border-radius: 3px;
        }

        .health-circle {
            width: 140px;
            height: 140px;
            margin: 0 auto;
            position: relative;
        }

        .health-circle svg {
            transform: rotate(-90deg);
        }

        .health-score-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }

        .health-score-text .score {
            font-size: 2.2rem;
            font-weight: 800;
        }

        .health-score-text .grade {
            font-size: 1rem;
            color: var(--text-dim);
        }

        .full-width {
            grid-column: 1 / -1;
        }

        footer {
            text-align: center;
            padding: 32px;
            color: var(--text-dim);
            font-size: 0.85rem;
            border-top: 1px solid var(--border);
        }

        footer a {
            color: var(--accent);
            text-decoration: none;
        }

        @media (max-width: 768px) {
            .header h1 { font-size: 1.8rem; }
            .metric-value { font-size: 1.8rem; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔭 RepoVision</h1>
        <p class="subtitle">{{ repo_name }} — Repository Analysis Report</p>
        <p style="color: var(--text-dim); margin-top: 8px; font-size: 0.85rem;">
            Generated on {{ generated_at }}
        </p>
    </div>

    <div class="container">

        <!-- Key Metrics -->
        <div class="grid">
            <div class="card">
                <h3>📦 Total Commits</h3>
                <div class="metric-value" style="color: var(--accent);">{{ total_commits }}</div>
                <div class="metric-label">across all branches</div>
            </div>
            <div class="card">
                <h3>👥 Contributors</h3>
                <div class="metric-value" style="color: var(--blue);">{{ contributor_count }}</div>
                <div class="metric-label">unique contributors</div>
            </div>
            <div class="card">
                <h3>📅 Repository Age</h3>
                <div class="metric-value" style="color: var(--green);">{{ age_display }}</div>
                <div class="metric-label">{{ branch_count }} branches</div>
            </div>
            <div class="card">
                <h3>🏥 Health Score</h3>
                <div class="metric-value" style="color: {{ health_color }};">{{ health_score }}/100</div>
                <div class="metric-label">Grade: {{ health_grade }}</div>
            </div>
        </div>

        <!-- Health Circle + Details -->
        <div class="grid">
            <div class="card" style="text-align: center;">
                <h3>Health Summary</h3>
                <div class="health-circle">
                    <svg width="140" height="140" viewBox="0 0 140 140">
                        <circle cx="70" cy="70" r="60" fill="none" stroke="var(--border)" stroke-width="12"/>
                        <circle cx="70" cy="70" r="60" fill="none"
                            stroke="{{ health_color }}" stroke-width="12"
                            stroke-dasharray="{{ health_dasharray }} 376.99"
                            stroke-linecap="round"/>
                    </svg>
                    <div class="health-score-text">
                        <div class="score" style="color: {{ health_color }};">{{ health_score }}</div>
                        <div class="grade">{{ health_grade }}</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <h3>Breakdown</h3>
                {{ health_details_html }}
            </div>
        </div>

        <!-- Weekly Activity Chart -->
        <div class="grid">
            <div class="card full-width">
                <h3>📊 Commit Activity by Day of Week</h3>
                <div class="chart-container">
                    <canvas id="weeklyChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Hourly Activity + Recent -->
        <div class="grid">
            <div class="card">
                <h3>⏰ Commits by Hour</h3>
                <div class="chart-container">
                    <canvas id="hourlyChart"></canvas>
                </div>
            </div>
            <div class="card">
                <h3>📅 Last 14 Days</h3>
                <div class="chart-container">
                    <canvas id="recentChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Top Files + Contributors -->
        <div class="grid">
            <div class="card">
                <h3>🔥 Code Hotspots</h3>
                <div style="max-height: 400px; overflow-y: auto;">
                    <table>
                        <thead>
                            <tr><th>File</th><th>Churn</th><th>Score</th><th>Authors</th></tr>
                        </thead>
                        <tbody>
                            {{ hotspots_rows }}
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="card">
                <h3>👥 Top Contributors</h3>
                <div style="max-height: 400px; overflow-y: auto;">
                    <table>
                        <thead>
                            <tr><th>Author</th><th>Commits</th><th>+Ins</th><th>-Del</th></tr>
                        </thead>
                        <tbody>
                            {{ contributors_rows }}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Languages -->
        <div class="grid">
            <div class="card full-width">
                <h3>🔤 Language Breakdown</h3>
                <div class="language-bar">
                    {{ language_bars }}
                </div>
                <div class="lang-legend">
                    {{ language_legend }}
                </div>
            </div>
        </div>

    </div>

    <footer>
        Generated by <a href="https://github.com/Stephen-pc/repovision">RepoVision</a> — Beautiful repository analytics
    </footer>

    <script>
    // ── Weekly Activity Chart ──
    new Chart(document.getElementById('weeklyChart'), {
        type: 'bar',
        data: {
            labels: {{ weekly_labels }},
            datasets: [{
                label: 'Commits',
                data: {{ weekly_data }},
                backgroundColor: ['{{ weekly_colors|safe }}'],
                borderRadius: 6,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(48,54,61,0.5)' }, ticks: { color: '#8b949e' } },
                x: { grid: { display: false }, ticks: { color: '#8b949e' } }
            }
        }
    });

    // ── Hourly Activity Chart ──
    new Chart(document.getElementById('hourlyChart'), {
        type: 'bar',
        data: {
            labels: {{ hourly_labels }},
            datasets: [{
                label: 'Commits',
                data: {{ hourly_data }},
                backgroundColor: 'rgba(108, 92, 231, 0.7)',
                borderRadius: 4,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(48,54,61,0.5)' }, ticks: { color: '#8b949e' } },
                x: { grid: { display: false }, ticks: { color: '#8b949e', maxTicksLimit: 12 } }
            }
        }
    });

    // ── Recent Activity Chart ──
    new Chart(document.getElementById('recentChart'), {
        type: 'line',
        data: {
            labels: {{ recent_labels }},
            datasets: [{
                label: 'Commits',
                data: {{ recent_data }},
                borderColor: '#74B9FF',
                backgroundColor: 'rgba(116, 185, 255, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 3,
                pointBackgroundColor: '#74B9FF',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(48,54,61,0.5)' }, ticks: { color: '#8b949e' } },
                x: { grid: { display: false }, ticks: { color: '#8b949e', maxTicksLimit: 7 } }
            }
        }
    });
    </script>
</body>
</html>"""


def _score_class(score: float) -> str:
    """Get CSS badge class for a hotspot score."""
    if score > 50:
        return "badge-high"
    elif score > 25:
        return "badge-medium"
    else:
        return "badge-low"


def generate_html_report(analysis: RepositoryAnalysis) -> str:
    """Generate a complete, self-contained HTML report.

    The report includes interactive Chart.js visualizations and a
    professional dark-theme design. No external dependencies are needed
    beyond the Chart.js CDN script included inline.

    Args:
        analysis: A fully populated RepositoryAnalysis object.

    Returns:
        Complete HTML document as a string.
    """
    health = analysis.health_score
    health_color = (
        "#00B894" if health["overall"] >= 70
        else "#FDCB6E" if health["overall"] >= 50
        else "#E17055"
    )
    circumference = 2 * 3.14159 * 60  # ~376.99
    health_dasharray = f"{(health['overall'] / 100) * circumference:.1f} {circumference}"

    # Age display
    if analysis.age_days > 365:
        age_display = f"{analysis.age_days / 365:.1f} years"
    elif analysis.age_days > 30:
        age_display = f"{analysis.age_days / 30:.0f} months"
    else:
        age_display = f"{analysis.age_days} days"

    # Health details HTML
    health_details_html = ""
    for key, value in health["details"].items():
        health_details_html += f'<div style="padding: 8px 0; border-bottom: 1px solid var(--border);">'
        health_details_html += f'<span style="color: var(--text-dim);">{key}</span><br>'
        health_details_html += f'<span style="font-weight: 600;">{value}</span></div>\n'

    # Weekly chart data
    weekly_labels = json.dumps(list(analysis.weekly_activity.keys()))
    weekly_data = json.dumps(list(analysis.weekly_activity.values()))
    # Color each day differently
    colors = ["#6C5CE7", "#74B9FF", "#00B894", "#FDCB6E", "#E17055", "#A29BFE", "#55EFC4"]
    weekly_colors = "','".join(colors[:7])

    # Hourly data
    hourly_labels = json.dumps([f"{h}:00" for h in range(24)])
    hourly_data = json.dumps([analysis.hourly_activity[h] for h in range(24)])

    # Recent data
    recent_labels = json.dumps(list(analysis.recent_activity.keys()))
    recent_data = json.dumps(list(analysis.recent_activity.values()))

    # Hotspots rows
    hotspots_rows = ""
    for h in analysis.hotspots[:10]:
        path = h["path"]
        if len(path) > 40:
            path = "…" + path[-39:]
        hotspots_rows += (
            f'<tr><td style="font-family: monospace; font-size: 0.8rem;">{path}</td>'
            f'<td>{h["churn"]}</td>'
            f'<td><span class="badge {_score_class(h["score"])}">{h["score"]}</span></td>'
            f'<td>{h["authors"]}</td></tr>\n'
        )

    # Contributors rows
    contributors_rows = ""
    for author in analysis.top_authors[:10]:
        contributors_rows += (
            f"<tr><td>{author.name[:30]}</td>"
            f"<td><strong>{author.commits}</strong></td>"
            f'<td style="color: var(--green);">+{author.insertions}</td>'
            f'<td style="color: var(--red);">-{author.deletions}</td></tr>\n'
        )

    # Language bars
    total_lines = sum(lang["lines"] for lang in analysis.languages) or 1
    language_bars = ""
    language_legend = ""
    for lang in analysis.languages:
        pct = (lang["lines"] / total_lines) * 100
        if pct < 1:
            continue
        language_bars += (
            f'<div style="flex: {pct:.0f} 0 0; background: {lang["color"]}; '
            f'min-width: 2px;" title="{lang["name"]}: {pct:.1f}%"></div>\n'
        )
        language_legend += (
            f'<div class="lang-item">'
            f'<div class="lang-dot" style="background: {lang["color"]};"></div>'
            f'{lang["name"]} {pct:.1f}%</div>\n'
        )

    # Fill template
    html = HTML_TEMPLATE
    html = html.replace("{{ repo_name }}", analysis.repo_name)
    html = html.replace("{{ generated_at }}", analysis.analyzed_at.strftime("%Y-%m-%d %H:%M"))
    html = html.replace("{{ total_commits }}", f"{analysis.total_commits:,}")
    html = html.replace("{{ contributor_count }}", str(analysis.contributor_count))
    html = html.replace("{{ branch_count }}", str(len(analysis.branches)))
    html = html.replace("{{ age_display }}", age_display)
    html = html.replace("{{ health_score }}", str(health["overall"]))
    html = html.replace("{{ health_grade }}", health["grade"])
    html = html.replace("{{ health_color }}", health_color)
    html = html.replace("{{ health_dasharray }}", health_dasharray)
    html = html.replace("{{ health_details_html }}", health_details_html)
    html = html.replace("{{ weekly_labels }}", weekly_labels)
    html = html.replace("{{ weekly_data }}", weekly_data)
    html = html.replace("{{ weekly_colors }}", weekly_colors)
    html = html.replace("{{ hourly_labels }}", hourly_labels)
    html = html.replace("{{ hourly_data }}", hourly_data)
    html = html.replace("{{ recent_labels }}", recent_labels)
    html = html.replace("{{ recent_data }}", recent_data)
    html = html.replace("{{ hotspots_rows }}", hotspots_rows)
    html = html.replace("{{ contributors_rows }}", contributors_rows)
    html = html.replace("{{ language_bars }}", language_bars)
    html = html.replace("{{ language_legend }}", language_legend)

    return html


def export_report(analysis: RepositoryAnalysis, output_path: Path) -> Path:
    """Export the analysis as an interactive HTML report.

    Args:
        analysis: A fully populated RepositoryAnalysis object.
        output_path: Where to write the HTML file.

    Returns:
        The path to the written file.
    """
    html = generate_html_report(analysis)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path
