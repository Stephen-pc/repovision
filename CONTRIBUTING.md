# Contributing to RepoVision

Thank you for your interest in contributing to RepoVision! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How to Contribute

### Types of Contributions

- **Bug Reports**: Help us identify and fix bugs
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit bug fixes or new features
- **Documentation**: Improve documentation
- **Testing**: Help test the software

### Where to Start

1. Check the [Issues](https://github.com/Stephen-pc/repovision/issues) page
2. Look for issues labeled `good first issue` or `help wanted`
3. Comment on the issue to let others know you're working on it

## Development Setup

### Prerequisites

- Python 3.9+
- Git 2.0+
- pip

### Setup Steps

1. **Fork and Clone**
   ```bash
   # Fork the repository on GitHub
   # Then clone your fork
   git clone https://github.com/YOUR_USERNAME/repovision.git
   cd repovision
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Verify Setup**
   ```bash
   # Run tests
   pytest
   
   # Check code style
   ruff check .
   ```

## Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for code formatting and linting.

### Style Guidelines

- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for public functions
- Keep functions focused and small
- Use meaningful variable names

### Formatting

```bash
# Check code style
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=repovision --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run specific test
pytest tests/test_core.py::test_function_name
```

### Writing Tests

- Write tests for all new features
- Write tests for bug fixes
- Aim for high test coverage
- Use descriptive test names
- Use fixtures for common setup

### Test Structure

```
tests/
├── conftest.py          # Shared fixtures
├── test_core.py         # Core module tests
├── test_cli.py          # CLI tests
├── test_display.py      # Display tests
└── test_report.py       # Report tests
```

## Pull Request Process

### Before Submitting

1. **Update Documentation**
   - Update README.md if needed
   - Add docstrings for new functions
   - Update CHANGELOG.md

2. **Run Tests**
   ```bash
   pytest
   ```

3. **Check Code Style**
   ```bash
   ruff check .
   ruff format .
   ```

4. **Test Your Changes**
   ```bash
   # Install locally
   pip install -e .
   
   # Test the CLI
   repovision
   repovision --quick
   ```

### Submitting PR

1. **Create Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Commit Changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

3. **Push to Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Fill in the PR template
   - Request review from maintainers

### PR Guidelines

- Keep PRs focused and small
- Write clear commit messages
- Include tests for new features
- Update documentation
- Be responsive to feedback

## Reporting Bugs

### Before Reporting

1. Check existing issues
2. Try the latest version
3. Reproduce the bug

### Bug Report Template

Use the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md) when creating issues.

Include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots if applicable

## Feature Requests

### Before Requesting

1. Check existing feature requests
2. Consider if it fits the project scope
3. Think about implementation

### Feature Request Template

Use the [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md) when creating issues.

Include:
- Problem description
- Proposed solution
- Alternatives considered
- Additional context

## Code Review Process

### What We Look For

- Correctness
- Test coverage
- Code style
- Documentation
- Performance
- Security

### Review Timeline

- Initial review within 48 hours
- Follow-up reviews as needed
- Merge after approval

## Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):
- MAJOR.MINOR.PATCH
- Breaking changes bump MAJOR
- New features bump MINOR
- Bug fixes bump PATCH

### Release Steps

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create release branch
4. Run tests
5. Create GitHub release
6. Publish to PyPI

## Questions?

If you have questions, feel free to:
- Open an issue
- Ask in discussions
- Contact maintainers

## Thank You!

Thank you for contributing to RepoVision! Your help makes this project better for everyone.
