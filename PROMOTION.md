# RepoVision 推广材料

## 📱 社交媒体文案（中文）

### V2EX / 掘金 / CSDN 帖子

**标题：** 分享一个超好看的 Git 仓库分析工具 🔭

**正文：**

大家好！我做了一个 Git 仓库分析的命令行工具，叫 **RepoVision**。

**主要功能：**
- 📊 终端里的精美仪表盘（Rich 绘制，超好看）
- 👥 贡献者分析和排名
- 🔥 代码热点检测（找出最容易出 bug 的文件）
- 📈 提交活动分析（按天、小时、最近 14 天趋势）
- 🏥 仓库健康评分（0-100 分）
- 📄 导出交互式 HTML 报告

**使用方法超简单：**
```bash
pip install repovision
cd your-project
repovision
```

**截图效果：**
（需要添加截图）

**项目地址：** https://github.com/Stephen-pc/repovision

技术栈：Python + Rich + Typer + GitPython

欢迎大家试用，觉得有用的话给个 star ⭐ 支持一下！

---

### Twitter / X 简短版本

```
🔭 Just released RepoVision — a beautiful CLI tool for git repository analytics!

✨ Features:
• Rich terminal dashboard
• Contributor insights
• Code hotspot detection
• Health scoring
• HTML report export

pip install repovision

GitHub: https://github.com/Stephen-pc/repovision

#Python #CLI #Git #DevTools #OpenSource
```

---

### Reddit /r/Python 帖子

**Title:** I built RepoVision — a beautiful CLI tool for git repository analytics

**Body:**

Hey r/Python! I wanted to share a tool I've been working on called **RepoVision**.

It's a command-line tool that gives you beautiful, insightful analytics for any git repository. Think of it as a health check dashboard for your codebase.

**Key Features:**
- 🎨 Rich terminal UI with charts and panels
- 👥 Contributor analysis and rankings
- 🔥 Code hotspot detection (frequently changed files)
- 📈 Commit activity patterns (by day, hour, trends)
- 🏥 Composite health score (0-100)
- 📄 Export to interactive HTML reports

**Quick start:**
```bash
pip install repovision
cd your-project
repovision
```

**What makes it different:**
- Pure Python, minimal dependencies
- Beautiful Rich-powered terminal output
- Smart hotspot detection using churn + recency scoring
- Self-contained HTML reports with Chart.js

I'd love to get your feedback! The project is MIT licensed and contributions are welcome.

**GitHub:** https://github.com/Stephen-pc/repovision

---

## 📝 中文论坛详细帖子（V2EX/掘金）

**标题：** [开源] RepoVision - 一个超好看的 Git 仓库分析 CLI 工具

**正文：**

### 项目简介

RepoVision 是一个用于分析 Git 仓库的命令行工具，可以生成精美的终端仪表盘和交互式 HTML 报告。

### 功能特性

1. **精美终端仪表盘**
   - 使用 Rich 库绘制，支持颜色和面板
   - 一目了然的仓库概览

2. **贡献者分析**
   - 查看每个人的提交数、代码行数、活跃天数
   - 支持排名和筛选

3. **代码热点检测**
   - 基于变更频率和最近活跃度的热点评分
   - 找出最容易出 bug 的文件
   - 帮助确定代码审查和重构的优先级

4. **提交活动分析**
   - 按星期几、小时统计提交模式
   - 最近 14 天的提交趋势（sparkline 图）

5. **仓库健康评分**
   - 综合评分（0-100）
   - 基于：最近活动 (30%)、贡献者多样性 (25%)、提交一致性 (25%)、变更分布 (20%)

6. **HTML 报告导出**
   - 交互式图表（Chart.js）
   - 深色主题，响应式设计
   - 自包含文件，方便分享

### 安装使用

```bash
# 安装
pip install repovision

# 使用
cd your-project
repovision

# 快速模式
repovision --quick

# 导出 HTML 报告
repovision --export report.html

# 分析热点文件
repovision hotspots

# 查看贡献者
repovision contributors
```

### 技术实现

- **Python 3.9+**
- **Rich** - 终端 UI 框架
- **Typer** - CLI 框架
- **GitPython** - Git 操作库
- **Chart.js** - HTML 报告图表

### 项目地址

https://github.com/Stephen-pc/repovision

### 欢迎贡献

项目采用 MIT 协议，欢迎提交 PR 和 Issue！

如果觉得有用，麻烦给个 star ⭐ 支持一下～

---

## 🎯 推广渠道清单

### 中文平台
- [ ] V2EX（创意工场节点）
- [ ] 掘金（开源项目标签）
- [ ] CSDN（开源中国社区）
- [ ] 知乎（回答相关问题）
- [ ] 微博（技术博主转发）
- [ ] 微信公众号（技术类）

### 英文平台
- [ ] Reddit /r/Python
- [ ] Reddit /r/commandline
- [ ] Reddit /r/programming
- [ ] Hacker News (Show HN)
- [ ] Dev.to
- [ ] Twitter/X
- [ ] LinkedIn

### GitHub 生态
- [ ] awesome-python 列表提交
- [ ] awesome-cli-apps 列表提交
- [ ] Python Weekly 提交
- [ ] Console Newsletter 提交

---

## 📸 截图建议

需要创建以下截图：

1. **主仪表盘截图** - 运行 `repovision` 的完整输出
2. **快速模式截图** - 运行 `repovision --quick` 的输出
3. **HTML 报告截图** - 浏览器中打开 HTML 报告的效果
4. **热点分析截图** - 运行 `repovision hotspots` 的输出

**截图命令：**
```bash
cd C:\Users\Steph\repovision
repovision > screenshots/dashboard.txt
repovision --quick > screenshots/quick.txt
repovision --export screenshots/report.html
repovision hotspots > screenshots/hotspots.txt
```

---

## 📊 发布检查清单

- [x] 代码完成
- [x] 测试通过（40个测试）
- [x] 推送到 GitHub
- [ ] 添加截图到 README
- [ ] 创建 PyPI 包（可选）
- [ ] 撰写推广帖子
- [ ] 发布到各个平台
- [ ] 提交到 awesome 列表
