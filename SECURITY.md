# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in RepoVision, please report it responsibly.

### How to Report

1. **Do NOT** create a public GitHub issue
2. Email security concerns to: [your-email@example.com]
3. Include detailed information about the vulnerability

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 1 week
- **Fix Release**: Depends on severity

### Disclosure Policy

- We will acknowledge receipt within 48 hours
- We will provide regular updates on progress
- We will notify you when the vulnerability is fixed
- We will credit you in the fix (unless you prefer anonymity)

## Security Best Practices

### For Users

- Keep RepoVision updated to the latest version
- Report any suspicious behavior immediately
- Do not run RepoVision on untrusted repositories without understanding the risks

### For Contributors

- Follow secure coding practices
- Validate all user inputs
- Use parameterized queries (if applicable)
- Keep dependencies updated
- Review code for security issues

## Scope

RepoVision is a read-only analytics tool. It:
- Reads git repository data
- Generates reports and visualizations
- Does NOT modify repository data
- Does NOT execute arbitrary code
- Does NOT access network resources (except for HTML report CDN links)

## Known Security Considerations

### HTML Reports

- HTML reports may contain JavaScript from Chart.js CDN
- Reports are self-contained and can be opened offline
- Be cautious when opening reports from untrusted sources

### Git Operations

- RepoVision uses GitPython for git operations
- All operations are read-only
- No remote operations are performed

## Contact

For security concerns, please contact:
- Email: [your-email@example.com]
- GitHub: https://github.com/Stephen-pc/repovision/security

## Acknowledgments

We thank all security researchers who responsibly disclose vulnerabilities.
