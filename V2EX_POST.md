# [开源] RepoVision - 一个超好看的 Git 仓库分析 CLI 工具

大家好！分享一个我最近做的 Git 仓库分析工具，叫 **RepoVision**。

## 功能特性

- 📊 **精美终端仪表盘** - 用 Rich 库绘制，支持颜色和图表
- 👥 **贡献者分析** - 查看每个人的提交数、代码行数、活跃天数
- 🔥 **代码热点检测** - 基于变更频率找出最容易出 bug 的文件
- 📈 **提交活动分析** - 按天、小时统计提交模式，14 天趋势图
- 🏥 **仓库健康评分** - 综合评分（0-100），包含详细分析
- 📄 **HTML 报告导出** - 交互式图表，方便分享

## 使用方法

```bash
# 安装
pip install repovision

# 使用（在任意 git 仓库目录下）
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

## 技术栈

- Python 3.9+
- Rich（终端 UI）
- Typer（CLI 框架）
- GitPython（Git 操作）

## 项目地址

https://github.com/Stephen-pc/repovision

## 截图

（运行 `repovision` 后会看到类似这样的效果）

```
╔═════════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║                        🔭 RepoVision  •  repovision                         ║
║                        Analyzed at 2026-06-07 01:55                         ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝
┌──────────────── 📊 Repository Overview ─────────────────┐
│  Repository: repovision                                 │
│  Branch:      master                                    │
│  Commits:      2                                        │
│  Contributors: 1                                        │
│  Health Score:  51/100 — D                              │
└─────────────────────────────────────────────────────────┘
```

## 特色功能

**代码热点检测：**
- 基于变更频率（60%）和最近活跃度（40%）的热点评分
- 帮助确定代码审查和重构的优先级

**仓库健康评分：**
- 最近活动 (30%)
- 贡献者多样性 (25%)
- 提交一致性 (25%)
- 变更分布 (20%)

---

欢迎试用！觉得有用的话给个 star ⭐ 支持一下～

有问题或建议欢迎提 Issue！
