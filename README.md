# Agent Bug Killer

> 通过构建线上 Bug 诊断 Agent，系统性掌握 AI Agent 开发全流程。

## 项目定位

这不是一个学习项目，而是一个**产品项目**。

每个阶段做一个真实可交付的 Agent 应用。从一个场景开始，逐步扩展，最终形成 Agent 开发的完整能力栈。

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

## 项目结构

```
agent-bug-killer/
├── README.md
├── roadmap.md                    # 详细路线图
├── tech-stack.md                 # 技术选型文档
├── pyproject.toml                # 项目配置
├── core/                         # Agent 核心框架（跨阶段复用）
│   ├── __init__.py
│   ├── base_agent.py             # Agent 基类
│   ├── base_tool.py              # Tool 基类
│   ├── memory.py                 # 记忆系统封装
│   └── planner.py                # 规划引擎封装
├── scenarios/                    # Agent 场景（每个场景独立）
│   ├── log-analyzer/             # 场景1: 日志分析器
│   │   ├── README.md
│   │   ├── src/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py          # LogAnalyzerAgent
│   │   │   ├── tools/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── file_reader.py
│   │   │   │   └── log_parser.py
│   │   │   └── prompts/
│   │   │       ├── system.md
│   │   │       └── diagnose.md
│   │   ├── cli.py                # 命令行入口
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py       # 测试 fixtures
│   │   │   ├── test_agent.py
│   │   │   ├── test_tools.py
│   │   │   └── test_integration.py
│   │   └── requirements.txt
│   │
│   ├── bug-diagnoser/            # 场景2: 线上Bug诊断器
│   │   ├── README.md
│   │   ├── src/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py          # BugDiagnoserAgent
│   │   │   ├── tools/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── ssh_tool.py
│   │   │   │   ├── cdp_tool.py
│   │   │   │   ├── log_parser.py
│   │   │   │   └── code_search.py
│   │   │   └── prompts/
│   │   │       ├── system.md
│   │   │       ├── diagnose.md
│   │   │       └── report.md
│   │   ├── cli.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   ├── test_agent.py
│   │   │   ├── test_ssh_tool.py
│   │   │   ├── test_cdp_tool.py
│   │   │   ├── test_integration.py
│   │   │   └── test_e2e.py
│   │   └── requirements.txt
│   │
│   └── scenario-3/               # 场景3: TBD
│       └── README.md
│
├── docs/                         # 开发笔记和设计文档
│   ├── decisions/                # 技术决策记录 (ADR)
│   └── learnings/                # 学习笔记
└── scripts/                      # 工具脚本
    └── run_tests.sh
```

## 开发原则

1. **场景独立**：每个 Agent 场景完全独立，可以单独运行和测试
2. **工具复用**：通用工具放在 core/ 下跨场景复用
3. **测试驱动**：每个功能先写测试，再写实现
4. **渐进式**：先跑通，再优化，最后产品化
5. **文档先行**：每个决策都记录下来，方便回顾和分享

## 快速开始

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆项目
cd d:/Code/agent-bug-killer

# 安装依赖
uv sync

# 运行测试
uv run pytest

# 运行场景1
uv run python scenarios/log-analyzer/cli.py --file /path/to/error.log
```
