# 提交到 awesome-python 列表

## 步骤

### 1. Fork awesome-python 仓库

访问 https://github.com/vinta/awesome-python 并点击 "Fork" 按钮。

### 2. 克隆你的 fork

```bash
git clone https://github.com/YOUR_USERNAME/awesome-python.git
cd awesome-python
```

### 3. 编辑 README.md

在 `README.md` 中找到合适的位置添加 RepoVision。

**建议位置：** 在 "Software" 或 "Dev Tools" 部分

找到类似这样的部分：
```markdown
## Software

- [cookiecutter](https://github.com/cookiecutter/cookiecutter) - A command-line utility that creates projects from cookiecutters (project templates).
```

在其后添加：
```markdown
- [RepoVision](https://github.com/Stephen-pc/repovision) - Beautiful git repository analytics at your fingertips. See contribution patterns, code hotspots, and team insights with a stunning terminal dashboard.
```

### 4. 提交更改

```bash
git add README.md
git commit -m "Add RepoVision to Software section

RepoVision is a beautiful CLI tool for git repository analytics that provides:
- Rich terminal dashboard
- Contributor insights
- Code hotspot detection
- Health scoring
- HTML report export"

git push origin main
```

### 5. 创建 Pull Request

1. 访问你 fork 的仓库
2. 点击 "Contribute" -> "Open pull request"
3. 填写 PR 标题：`Add RepoVision to Software section`
4. 填写 PR 描述：

```markdown
## What is this PR?

Adding RepoVision to the Software section.

## What is RepoVision?

RepoVision is a beautiful CLI tool for git repository analytics that provides:

- 📊 Rich terminal dashboard with charts and panels
- 👥 Contributor analysis and rankings
- 🔥 Code hotspot detection (churn + recency scoring)
- 📈 Commit activity analysis (by day, hour, 14-day trends)
- 🏥 Repository health scoring (0-100)
- 📄 Interactive HTML report export with Chart.js

## Installation

```bash
pip install repovision
```

## Links

- GitHub: https://github.com/Stephen-pc/repovision
- PyPI: https://pypi.org/project/repovision/
```

5. 点击 "Create pull request"

## 其他 Awesome 列表

### awesome-cli-apps

1. Fork https://github.com/agarrharr/awesome-cli-apps
2. 在 "Development" 部分添加 RepoVision
3. 提交 PR

### awesome-python-applications

1. Fork https://github.com/mahmoud/awesome-python-applications
2. 在合适的位置添加 RepoVision
3. 提交 PR

## 注意事项

- 确保你的 PR 符合 awesome 列表的贡献指南
- 保持描述简洁明了
- 使用正确的格式（通常是 `- [Name](url) - Description.`）
- 等待维护者审核和合并

## 预期结果

- PR 被合并后，你的项目会出现在 awesome 列表中
- 这会带来持续的曝光和 star
- 通常需要几天到几周的时间被合并
