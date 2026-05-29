# Agent Bug Killer

> AI-Powered Bug Diagnosis Agent — 不只监控，更要诊断

[![CI](https://github.com/your-org/agent-bug-killer/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/agent-bug-killer/actions)
[![Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen)](https://github.com/your-org/agent-bug-killer)
[![Python](https://img.shields.io/badge/python-3.12+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 项目定位

这不是一个学习项目，而是一个**产品项目**。

Agent Bug Killer 是一个 AI 驱动的 Bug 诊断系统，帮助开发者更快地识别和修复线上问题。
它使用多数据源（日志、服务器、浏览器、代码）提供智能诊断。

## 核心特性

### 🤖 AI 驱动诊断
- 自动根因分析（RCA）
- 多源数据关联
- 智能修复建议
- 知识库学习

### 🔧 多源数据采集
- SSH 远程命令执行
- CDP 浏览器调试
- 日志文件分析
- 源代码搜索

### 📊 结构化输出
- JSON 格式报告
- Markdown 格式报告
- HTML 格式报告
- 诊断历史记录

### 🚀 生产就绪
- FastAPI Web API
- Docker 容器化
- GitHub Actions CI/CD
- 完整测试覆盖

## 技术栈

| 层级 | 选型 | 理由 |
|------|------|------|
| **框架** | LangChain DeepAgents | 官方框架，开箱即用的 planning、memory、sub-agent |
| **LLM** | Claude API (via LangChain) | Tool Use 原生支持，中文能力强 |
| **运行时** | LangGraph | DeepAgents 底层，提供状态管理和持久化 |
| **语言** | Python 3.12+ | AI 生态最完整 |
| **包管理** | uv | 现代、快速，DeepAgents 官方推荐 |
| **测试** | pytest + pytest-asyncio | Python 标准测试框架 |
| **部署** | Docker | 标准化部署 |

## 快速开始

### 安装

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆项目
git clone https://github.com/your-org/agent-bug-killer.git
cd agent-bug-killer

# 安装依赖
uv sync

# 配置环境
cp .env.example .env
# 编辑 .env 填入 API 密钥
```

### 使用 CLI

```bash
# 分析日志文件
uv run python scenarios/log_analyzer/cli.py --file /path/to/error.log

# 诊断 Bug
uv run python scenarios/bug_diagnoser/cli.py \
  --bug "页面白屏" \
  --host prod-server \
  --user deploy

# 输出 Markdown 报告
uv run python scenarios/log_analyzer/cli.py \
  --file error.log \
  --output report.md \
  --format markdown
```

### 使用 API

```bash
# 启动 API 服务
uv run uvicorn api:app --reload

# 访问 API 文档
open http://localhost:8000/docs
```

### 使用 Python

```python
from scenarios.log_analyzer.src.agent import analyze_log
from scenarios.bug_diagnoser.src.agent import diagnose_bug

# 分析日志
result = analyze_log("/path/to/error.log")

# 诊断 Bug
result = diagnose_bug(
    bug_description="页面白屏",
    server_info={"host": "prod-server", "user": "deploy"},
)
```

## 核心模块

| 模块 | 功能 | 测试 |
|------|------|------|
| base_agent.py | Agent 工厂 | ✅ |
| base_tool.py | Tool 工具 | ✅ |
| settings.py | 配置管理 | ✅ |
| prompt_loader.py | Prompt 加载 | ✅ |
| memory.py | 记忆系统 | ✅ |
| planner.py | 规划助手 | ✅ |
| formatters.py | 输出格式 | ✅ |
| history.py | 诊断历史 | ✅ |
| analyzer.py | 根因分析 | ✅ |
| knowledge_base.py | 知识库 | ✅ |
| fix_suggestions.py | 修复建议 | ✅ |
| error_groups.py | 错误分组 | ✅ |
| rca_engine.py | RCA 引擎 | ✅ |
| metrics.py | 指标收集 | ✅ |
| retry.py | 重试逻辑 | ✅ |
| validators.py | 输入验证 | ✅ |
| progress.py | 进度跟踪 | ✅ |
| exceptions.py | 自定义异常 | ✅ |
| cache.py | 缓存工具 | ✅ |

## 测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试
uv run pytest scenarios/log_analyzer/tests/

# 运行覆盖率报告
uv run pytest --cov=core --cov=scenarios --cov=api --cov-report=html

# 运行 lint
uv run ruff check .

# 运行类型检查
uv run mypy core/ scenarios/ api/
```

### 测试指标

| 指标 | 值 |
|------|-----|
| 测试数量 | 284 |
| 测试通过率 | 100% |
| 代码覆盖率 | 92% |
| Mypy 错误 | 0 |
| Lint 错误 | 0 |

## API 端点

| 端点 | 方法 | 功能 |
|------|------|------|
| /health | GET | 健康检查 |
| /api/v1/analyze-log | POST | 日志分析 |
| /api/v1/diagnose | POST | Bug 诊断 |
| /api/v1/history | GET | 历史列表 |
| /api/v1/history/{id} | GET | 获取报告 |
| /api/v1/history/{id} | DELETE | 删除报告 |
| /api/v1/history/search/{q} | GET | 搜索历史 |
| /api/v1/knowledge | GET | 知识库列表 |
| /api/v1/knowledge/{id} | GET | 获取知识条目 |
| /api/v1/knowledge/search/{q} | GET | 搜索知识库 |

## 文档

- [Getting Started](docs/getting-started.md) - 快速开始
- [API Reference](docs/api-reference.md) - API 参考
- [Best Practices](docs/best-practices.md) - 最佳实践
- [FAQ](docs/faq.md) - 常见问题
- [Architecture](docs/architecture-v2.md) - 系统架构
- [Competitor Analysis](docs/competitor-analysis.md) - 竞品分析
- [Roadmap](docs/roadmap-v2.md) - 产品路线图
- [Community](docs/community.md) - 社区指南

## 竞品对比

| 特性 | Agent Bug Killer | Sentry | Datadog | LangSmith |
|------|------------------|--------|---------|-----------|
| AI 根因分析 | ✅ | ❌ | 部分 | ❌ |
| 多源关联 | ✅ | ❌ | ✅ | ❌ |
| 修复建议 | ✅ | ❌ | ❌ | ❌ |
| 知识库 | ✅ | ❌ | ❌ | ❌ |
| 开源 | ✅ | ✅ | ❌ | ❌ |
| 本地部署 | ✅ | ✅ | ❌ | ❌ |

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 贡献方式

1. 报告 Bug
2. 建议新功能
3. 提交代码
4. 改进文档
5. 分享知识

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE)。

## 致谢

感谢所有贡献者！

## 联系方式

- Issues: [GitHub Issues](https://github.com/your-org/agent-bug-killer/issues)
- Discussions: [GitHub Discussions](https://github.com/your-org/agent-bug-killer/discussions)
- Documentation: [docs/](docs/)
