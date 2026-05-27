# Agent Bug Killer 技术选型文档

## 选型决策

### 1. Agent 框架：LangChain DeepAgents

**选择理由**：

| 考量 | DeepAgents | 手写 Agent | LangGraph 单独用 |
|------|-----------|-----------|-----------------|
| 上手速度 | 快（开箱即用） | 慢（从零造轮子） | 中 |
| 功能完整度 | 高（planning/memory/sub-agent） | 低（需要自己实现） | 中 |
| 学习价值 | 高（学习工业级架构） | 高（理解底层原理） | 高 |
| 灵活性 | 中（框架约束） | 高（完全自由） | 高 |
| 社区支持 | 强（LangChain 生态） | 无 | 强 |

**决策**：Phase 1-2 使用 DeepAgents，Phase 3 根据需要降级到 LangGraph。

**官方仓库**：https://github.com/langchain-ai/deepagents

**核心 API**：

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[my_tool_1, my_tool_2],
    system_prompt="You are a ...",
)

result = agent.invoke({"messages": "..."})
```

**DeepAgents 提供的核心能力**：

| 能力 | 说明 | 我们的使用方式 |
|------|------|---------------|
| Planning | 自动分解任务为多步计划 | 诊断流程的自动规划 |
| Filesystem | 文件读写工具 | 读取日志文件 |
| Shell | 命令执行工具 | SSH 命令执行 |
| Sub-agents | 子 Agent 委托 | 复杂诊断委托给专用 Agent |
| Memory | 跨会话记忆 | 诊断历史记录 |
| Middleware | 中间件系统 | 日志、重试、权限控制 |
| Human-in-the-loop | 人工介入 | 敏感操作确认 |
| Skills | 可加载的技能 | 诊断知识库 |

### 2. LLM：Claude API

**选择理由**：

| 考量 | Claude API | OpenAI API | 本地模型 |
|------|-----------|-----------|---------|
| Tool Use 支持 | 原生、优秀 | 支持但不如 Claude | 有限 |
| 中文能力 | 强 | 中 | 弱 |
| 长上下文 | 200K tokens | 128K tokens | 取决于模型 |
| 价格 | 中等 | 中等 | 免费 |
| 生态集成 | LangChain 原生支持 | LangChain 原生支持 | 需要额外配置 |

**决策**：使用 Claude API，通过 LangChain 集成。

**模型选择**：

| 模型 | 用途 | 价格 |
|------|------|------|
| `claude-sonnet-4-6` | 主力模型（Agent 推理） | $3/$15 per 1M tokens |
| `claude-haiku-4-5` | 轻量任务（日志解析） | $0.25/$1.25 per 1M tokens |

**成本预估**（每次诊断）：

```
Phase 1 (日志分析):
- 输入: ~2K tokens (日志 + prompt)
- 输出: ~1K tokens (诊断报告)
- 成本: ~$0.02/次

Phase 2 (Bug诊断):
- 输入: ~5K tokens (日志 + 截图描述 + prompt)
- 输出: ~2K tokens (诊断报告)
- 成本: ~$0.05/次
```

### 3. 包管理：uv

**选择理由**：

| 考量 | uv | pip + venv | poetry |
|------|-----|-----------|--------|
| 速度 | 极快（Rust 实现） | 慢 | 中 |
| DeepAgents 官方推荐 | 是 | 否 | 否 |
| Lock 文件 | 支持 | 不支持 | 支持 |
| Python 版本管理 | 支持 | 不支持 | 支持 |

**决策**：使用 uv，与 DeepAgents 官方保持一致。

### 4. 测试框架：pytest

**选择理由**：

| 考量 | pytest | unittest |
|------|--------|----------|
| 语法简洁 | 是（装饰器、fixture） | 否（class 继承） |
| 异步支持 | pytest-asyncio | 需要额外配置 |
| Mock 支持 | pytest-mock | unittest.mock |
| 社区生态 | 最大 | 标准库 |

**测试依赖**：

```
pytest
pytest-asyncio      # 异步测试支持
pytest-mock         # Mock 支持
pytest-cov          # 覆盖率报告
respx               # HTTP 请求 mock（用于 LLM API）
```

### 5. SSH 库：Paramiko

**选择理由**：

| 考量 | Paramiko | subprocess + sshpass | Fabric |
|------|---------|---------------------|--------|
| 纯 Python | 是 | 否（依赖系统 ssh） | 是 |
| 功能完整 | 高 | 低 | 高 |
| 异步支持 | 有（paramiko-ng） | 无需 | 有 |
| 学习成本 | 中 | 低 | 低 |

**决策**：使用 Paramiko，纯 Python 实现，不依赖系统 SSH。

### 6. CDP 库：playwright 或 pyppeteer

**选择理由**：

| 考量 | Playwright | pyppeteer | 直接 WebSocket |
|------|-----------|-----------|---------------|
| 维护状态 | 活跃 | 不活跃 | N/A |
| 异步支持 | 原生异步 | 原生异步 | 需要手动 |
| 功能完整 | 高 | 中 | 低 |
| 安装复杂度 | 中 | 低 | 低 |

**决策**：Phase 2 再确定。先关注 Agent 逻辑，CDP 工具可以先用简单的 WebSocket 实现。

### 7. 日志解析：正则 + LLM

**策略**：

```
第一层：正则提取（快速、低成本）
  - 提取 ERROR/WARNING 级别日志
  - 提取堆栈信息
  - 提取时间戳和模块名

第二层：LLM 分析（深度、智能）
  - 理解错误上下文
  - 关联已知问题
  - 生成诊断报告
```

**理由**：正则处理结构化信息（快且便宜），LLM 处理非结构化理解（慢但智能）。

---

## 依赖清单

### 核心依赖

```toml
[project]
dependencies = [
    "langchain>=0.3",
    "langchain-anthropic>=0.3",
    "langchain-core>=0.3",
    "deepagents>=0.1",
    "paramiko>=3.4",
    "pydantic>=2.0",
    "rich>=13.0",          # CLI 美化
    "click>=8.0",          # CLI 框架
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "pytest-mock>=3.14",
    "pytest-cov>=5.0",
    "respx>=0.21",
    "ruff>=0.6",           # 代码检查
]
```

### 版本约束

- Python: >= 3.12（DeepAgents 要求）
- uv: 最新版
- Node.js: 可选（如果用 Playwright）

---

## 环境配置

### 环境变量

```bash
# .env 文件
ANTHROPIC_API_KEY=sk-ant-...        # Claude API 密钥

# Phase 2 可选
SSH_KEY_PATH=~/.ssh/id_rsa          # SSH 密钥路径
CDP_BROWSER_WS=ws://...            # CDP 连接地址
```

### 配置文件

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM
    llm_model: str = "anthropic:claude-sonnet-4-6"
    llm_fallback_model: str = "anthropic:claude-haiku-4-5"
    
    # SSH
    ssh_timeout: int = 30
    ssh_max_retries: int = 3
    
    # CDP
    cdp_timeout: int = 10
    cdp_screenshot_dir: str = "/tmp/agent-bug-killer/screenshots"
    
    # 日志
    log_max_lines: int = 500
    log_max_tokens: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 开发工具

| 工具 | 用途 | 安装 |
|------|------|------|
| uv | 包管理 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| ruff | 代码检查和格式化 | `uv add ruff` |
| mypy | 类型检查 | `uv add mypy` |
| pre-commit | Git hooks | `uv add pre-commit` |

### 代码规范

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.12"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```
