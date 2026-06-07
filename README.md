<h1 align="center">
  🔭 RepoVision
</h1>

<p align="center">
  <strong>Beautiful git repository analytics at your fingertips.</strong>
</p>

<p align="center">
  <a href="#-installation"><img src="https://img.shields.io/badge/pip-install-blue?style=flat-square&logo=pypi"></a>
  <a href="https://github.com/Stephen-pc/repovision/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.9%2B-blue?style=flat-square&logo=python"></a>
  <a href="#"><img src="https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey?style=flat-square"></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Stephen-pc/repovision/main/screenshots/dashboard.png" alt="RepoVision Dashboard" width="800">
</p>

> 💡 **Tip:** Run `repovision` in your terminal to see the full interactive dashboard!

---

**RepoVision** gives you deep, beautiful insights into any git repository — right in your terminal. See contribution patterns, identify code hotspots, track team activity, and export stunning interactive HTML reports. All with a single command.

## ✨ Features

- 📊 **Rich Terminal Dashboard** — A gorgeous, colorful overview of your repository with charts and panels
- 👥 **Contributor Insights** — See who's contributing, how much, and when
- 🔥 **Code Hotspot Detection** — Find files that change most frequently — your bug-risk zones
- 📈 **Activity Analytics** — Commit frequency by day, hour, and over time with sparkline visualizations
- 🏥 **Health Scoring** — Get a composite health score (0–100) with detailed breakdown
- 🔤 **Language Detection** — Auto-detect programming languages with a colorful breakdown
- 📄 **HTML Report Export** — Generate beautiful, interactive HTML reports with Chart.js
- ⚡ **Blazing Fast** — Smart caching, minimal dependencies, pure Python
- 🎨 **GitHub-style Design** — Dark theme inspired by GitHub's design language

## 📦 Installation

```bash
pip install repovision
```

> **Requirements:** Python 3.9+, Git 2.0+

### From source

```bash
git clone https://github.com/Stephen-pc/repovision.git
cd repovision
pip install -e .
```

## 🚀 Quick Start

```bash
# Go to any git repository
cd your-project

# See the full dashboard
repovision

# Quick one-line stats
repovision --quick

# Export an interactive HTML report
repovision --export report.html

# Analyze a different repo
repovision --path /path/to/another/repo

# Analyze more commit history
repovision --commits 2000
```

## 📖 Usage

### Full Dashboard

```bash
repovision
```

Shows a beautiful multi-panel dashboard with:
- Repository overview & key metrics
- Health score with detailed breakdown
- Commit activity by day of week and hour
- Recent activity sparkline (14 days)
- Code hotspots ranked by churn + recency
- Top contributors table
- Language breakdown

### Quick Stats

```bash
repovision --quick
# or: repovision quick
```

Compact one-line summary — perfect for shell prompts or scripts.

### Export HTML Report

```bash
repovision --export report.html
# or: repovision export report.html
```

Generates a self-contained, interactive HTML report with Chart.js visualizations. Dark themed, responsive, and ready to share.

### Hotspot Analysis

```bash
repovision hotspots
repovision hotspots --top 20
```

Identify files that change frequently — these are your refactoring candidates and bug-risk areas.

### Contributor Analysis

```bash
repovision contributors
repovision contributors --top 20
```

See who's contributing, including insertions, deletions, files touched, and active days.

## 🏥 Health Score

RepoVision computes a composite health score (0–100) based on:

| Factor | Weight | What it measures |
|--------|--------|-----------------|
| **Recent Activity** | 30% | Commits in the last 30 days |
| **Contributor Diversity** | 25% | Number of unique contributors |
| **Commit Consistency** | 25% | Average commits per week over the repo's lifetime |
| **Churn Distribution** | 20% | Whether changes are spread across files or concentrated |

**Grading scale:** A+ (90+) · A (80–89) · B (70–79) · C (60–69) · D (50–59) · F (0–49)

## 🔥 Hotspot Detection

Hotspots are files that combine **high churn** (frequent changes) with **recent activity**. These are your highest-risk files — great candidates for:
- Code review prioritization
- Test coverage improvement
- Refactoring
- Architectural review

The hotspot score (0–100) weights churn at 60% and recency at 40%.

## 📁 Project Structure

```
repovision/
├── repovision/
│   ├── __init__.py          # Package metadata
│   ├── __main__.py          # python -m repovision support
│   ├── cli.py               # CLI commands (Typer)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── git_utils.py     # Low-level git operations
│   │   └── analyzer.py      # Analysis engine
│   └── display/
│       ├── __init__.py
│       ├── terminal.py      # Rich terminal dashboard
│       └── html_report.py   # HTML report generation
├── tests/
│   ├── conftest.py          # Shared test fixtures
│   ├── test_core.py         # Core module tests
│   ├── test_cli.py          # CLI tests
│   ├── test_display.py      # Display tests
│   └── test_report.py       # Report tests
├── pyproject.toml            # Project configuration
├── LICENSE                   # MIT License
├── .gitignore
└── README.md                 # You are here!
```

## 🧪 Development

```bash
# Clone and install dev dependencies
git clone https://github.com/Stephen-pc/repovision.git
cd repovision
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=repovision --cov-report=html
```

## 🤝 Contributing

Contributions are welcome! Here's how to help:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to your branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

Please ensure tests pass and add tests for new features.

## 📜 License

MIT © RepoVision Contributors

## ⭐ Star History

If you find RepoVision useful, please consider [giving it a star ⭐](https://github.com/Stephen-pc/repovision) — it helps others discover the project!

---

<p align="center">
  <sub>Built with ❤️ using Python, Rich, Typer, and GitPython</sub>
</p>
