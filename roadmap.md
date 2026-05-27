# Agent Bug Killer 开发路线图

## 总览

```
Phase 1 (2周)          Phase 2 (3周)          Phase 3 (4周)
日志分析器              线上Bug诊断器           产品级Agent
─────────────          ─────────────          ─────────────
掌握Agent基础           掌握工具编排            掌握架构设计
                                              
DeepAgents入门         多工具协调              多Agent协作
Tool Use               多步规划                记忆系统
Prompt设计             错误恢复                部署运维
单元测试               结构化输出              用户体验
```

---

## Phase 1: 日志分析器 (Log Analyzer)

### 目标

跑通一个完整的 DeepAgent 循环，掌握核心概念。

### 学习目标

| 概念 | 具体内容 | 验证方式 |
|------|---------|---------|
| DeepAgents 基础 | `create_deep_agent()` 使用 | Agent 能正确调用工具 |
| Tool Use | 定义和注册自定义工具 | 工具能被 Agent 正确调用 |
| Prompt Engineering | System Prompt 设计 | Agent 行为符合预期 |
| 单元测试 | pytest 基础、mock LLM 调用 | 测试覆盖率 > 80% |
| 错误处理 | 工具调用失败时的降级 | 异常场景测试通过 |

### 功能范围

```
输入: error.log 文件路径（或直接传入日志文本）
Agent: 
  1. 读取日志文件（file_reader 工具）
  2. 解析日志，提取关键错误信息（log_parser 工具）
  3. 分析错误模式，关联已知问题
  4. 输出结构化诊断摘要
输出: JSON 格式的诊断报告
```

### 工具清单

| 工具 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `file_reader` | 读取文件内容 | file_path: str | content: str |
| `log_parser` | 解析日志提取错误 | content: str | errors: list[dict] |

### 任务分解

```
Week 1:
├── Day 1-2: 项目骨架搭建
│   ├── 初始化项目结构
│   ├── 配置 pyproject.toml + uv
│   └── 编写 core/base_agent.py, core/base_tool.py
│
├── Day 3-4: 工具开发
│   ├── 实现 file_reader 工具
│   ├── 实现 log_parser 工具
│   └── 为每个工具编写单元测试
│
└── Day 5: Agent 主逻辑
    ├── 编写 LogAnalyzerAgent
    ├── 设计 System Prompt
    └── 编写 Agent 单元测试（mock LLM）

Week 2:
├── Day 1-2: 集成测试
│   ├── 编写集成测试（真实 LLM 调用）
│   ├── 准备测试用的日志样本
│   └── 验证 Agent 端到端流程
│
├── Day 3-4: CLI 入口 + 优化
│   ├── 实现 CLI 命令行入口
│   ├── 优化 Prompt（根据测试结果）
│   └── 添加日志和错误处理
│
└── Day 5: 文档 + 复盘
    ├── 编写场景 README
    ├── 记录技术决策 (ADR)
    └── 学习笔记
```

### 测试策略

#### 单元测试 (Phase 1 期间完成)

| 测试对象 | 测试内容 | Mock 策略 |
|----------|---------|----------|
| `file_reader` | 读取存在的文件 | 无需 mock |
| `file_reader` | 文件不存在时的错误处理 | 无需 mock |
| `file_reader` | 文件过大时的截断 | 无需 mock |
| `log_parser` | 提取 ERROR 级别日志 | 无需 mock |
| `log_parser` | 提取堆栈信息 | 无需 mock |
| `log_parser` | 空日志文件处理 | 无需 mock |
| `LogAnalyzerAgent` | 正确调用 file_reader | Mock LLM 返回工具调用 |
| `LogAnalyzerAgent` | 正确调用 log_parser | Mock LLM 返回工具调用 |
| `LogAnalyzerAgent` | 工具调用失败时的处理 | Mock 工具抛异常 |
| `LogAnalyzerAgent` | 输出格式正确 | Mock LLM 返回最终答案 |

#### 集成测试 (Phase 1 第二周)

| 测试场景 | 输入 | 预期输出 |
|----------|------|---------|
| Python 异常日志 | 包含 Traceback 的日志 | 识别异常类型和位置 |
| 多行堆栈日志 | 跨多行的错误堆栈 | 正确提取完整堆栈 |
| 混合级别日志 | INFO/WARNING/ERROR 混合 | 只关注 ERROR |
| 空日志文件 | 空文件 | 返回"无错误" |

#### 测试文件结构

```
tests/
├── __init__.py
├── conftest.py              # 共享 fixtures
│   ├── sample_logs/         # 测试用日志样本
│   │   ├── python_exception.log
│   │   ├── multiline_stack.log
│   │   ├── mixed_levels.log
│   │   └── empty.log
│   └── mock_llm.py          # Mock LLM 工具
├── test_file_reader.py      # file_reader 单元测试
├── test_log_parser.py       # log_parser 单元测试
├── test_agent.py            # Agent 单元测试（mock LLM）
└── test_integration.py      # 集成测试（真实 LLM）
```

### 验收标准

- [ ] Agent 能正确读取日志文件
- [ ] Agent 能正确解析并提取错误信息
- [ ] Agent 输出结构化 JSON 诊断报告
- [ ] 单元测试覆盖率 > 80%
- [ ] 集成测试全部通过
- [ ] CLI 可正常运行
- [ ] README 和 ADR 编写完成

---

## Phase 2: 线上 Bug 诊断器 (Bug Diagnoser)

### 目标

掌握多工具编排和复杂场景下的 Agent 设计。

### 前置条件

- Phase 1 已完成
- 有一台可 SSH 访问的测试服务器
- 有一个可 CDP 连接的浏览器

### 学习目标

| 概念 | 具体内容 | 验证方式 |
|------|---------|---------|
| 多工具协调 | Agent 按需选择和组合工具 | 复杂场景测试通过 |
| 多步规划 | Agent 制定诊断计划并执行 | 诊断流程合理 |
| 错误恢复 | 工具调用失败时的降级策略 | 异常场景测试通过 |
| 结构化输出 | 诊断报告格式化 | 输出格式一致 |
| 权限控制 | SSH/CDP 连接的安全管理 | 安全测试通过 |

### 功能范围

```
输入: Bug 描述 + 服务器信息 + 浏览器地址
Agent:
  1. 并行收集信息:
     - SSH → 检查应用日志、进程状态、端口占用
     - CDP → 截图、Console 日志、Network 请求
  2. 分析阶段:
     - 提取错误关键词
     - 分类错误类型（JS报错/网络错误/渲染异常）
     - 关联代码位置
  3. 输出阶段:
     - 生成诊断报告
     - 给出修复建议
输出: 结构化诊断报告（Markdown 格式）
```

### 工具清单

| 工具 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `ssh_exec` | SSH 执行远程命令 | host, user, password/key, command | result: str |
| `ssh_read_log` | 读取远程日志文件 | host, user, password/key, path, lines | content: str |
| `cdp_connect` | 连接浏览器 | ws_url: str | session_id: str |
| `cdp_screenshot` | 浏览器截图 | session_id: str | screenshot_path: str |
| `cdp_console` | 获取 Console 日志 | session_id: str | logs: list[dict] |
| `cdp_network` | 获取网络请求 | session_id: str | requests: list[dict] |
| `log_parser` | 解析日志（复用 Phase 1） | content: str | errors: list[dict] |
| `code_search` | 搜索代码 | pattern: str, path: str | matches: list[dict] |

### 任务分解

```
Week 1: SSH 工具 + 测试
├── Day 1-2: SSH 工具开发
│   ├── 实现 ssh_exec 工具
│   ├── 实现 ssh_read_log 工具
│   ├── SSH 连接管理（连接池、超时、重试）
│   └── 安全设计（密钥管理、会话清理）
│
├── Day 3-4: SSH 工具测试
│   ├── 单元测试：mock SSH 连接
│   ├── 集成测试：真实 SSH 连接（测试服务器）
│   └── 安全测试：连接超时、认证失败
│
└── Day 5: 代码搜索工具
    ├── 实现 code_search 工具
    └── 单元测试

Week 2: CDP 工具 + 测试
├── Day 1-2: CDP 工具开发
│   ├── 实现 cdp_connect 工具
│   ├── 实现 cdp_screenshot 工具
│   ├── 实现 cdp_console 工具
│   ├── 实现 cdp_network 工具
│   └── CDP 连接管理（重连、超时）
│
├── Day 3-4: CDP 工具测试
│   ├── 单元测试：mock CDP 连接
│   ├── 集成测试：真实 CDP 连接（本地浏览器）
│   └── 异常测试：浏览器关闭、页面跳转
│
└── Day 5: 工具集成测试
    ├── 多工具并行调用测试
    └── 工具组合测试

Week 3: Agent 主逻辑 + 端到端
├── Day 1-2: Agent 开发
│   ├── 实现 BugDiagnoserAgent
│   ├── 设计诊断流程 Prompt
│   ├── 实现并行工具调用
│   └── 实现诊断报告生成
│
├── Day 3: 端到端测试
│   ├── 准备测试场景（模拟线上bug）
│   ├── 端到端流程测试
│   └── 性能测试（诊断耗时）
│
└── Day 4-5: CLI + 文档
    ├── 实现 CLI 入口
    ├── 优化 Prompt
    ├── 编写 README
    └── 学习笔记
```

### 测试策略

#### 单元测试

| 测试对象 | 测试内容 | Mock 策略 |
|----------|---------|----------|
| `ssh_exec` | 成功执行命令 | Mock paramiko.SSHClient |
| `ssh_exec` | 连接超时 | Mock 连接超时异常 |
| `ssh_exec` | 认证失败 | Mock 认证异常 |
| `ssh_exec` | 命令执行超时 | Mock 命令超时 |
| `ssh_read_log` | 读取日志文件 | Mock SSH + 文件内容 |
| `cdp_connect` | 成功连接浏览器 | Mock websocket |
| `cdp_connect` | 连接失败 | Mock 连接异常 |
| `cdp_screenshot` | 成功截图 | Mock CDP 响应 |
| `cdp_console` | 获取 Console 日志 | Mock CDP 响应 |
| `cdp_network` | 获取网络请求 | Mock CDP 响应 |
| `code_search` | 搜索匹配的代码 | Mock 文件系统 |
| `BugDiagnoserAgent` | 正确规划诊断步骤 | Mock LLM |
| `BugDiagnoserAgent` | 并行调用多个工具 | Mock LLM + 工具 |
| `BugDiagnoserAgent` | 工具失败时的降级 | Mock 工具异常 |
| `BugDiagnoserAgent` | 输出格式正确 | Mock LLM |

#### 集成测试

| 测试场景 | 输入 | 预期行为 |
|----------|------|---------|
| SSH 连接成功 | 有效的服务器信息 | 能执行命令并返回结果 |
| SSH 连接失败 | 无效的服务器信息 | 返回明确的错误信息 |
| CDP 连接成功 | 运行中的浏览器 | 能截图和获取日志 |
| CDP 连接失败 | 未运行的浏览器 | 返回明确的错误信息 |
| 完整诊断流程 | Bug 描述 + 测试服务器 | 输出完整诊断报告 |

#### E2E 测试

| 场景 | 模拟方式 | 验证点 |
|------|---------|--------|
| 前端白屏 | 测试页面注入 JS 错误 | Agent 能定位到 JS 错误 |
| 接口超时 | 测试服务器模拟慢响应 | Agent 能发现网络问题 |
| 进程崩溃 | 测试服务器 kill 进程 | Agent 能发现进程异常 |

#### 测试文件结构

```
tests/
├── __init__.py
├── conftest.py
│   ├── fixtures/
│   │   ├── mock_ssh.py          # Mock SSH 连接
│   │   ├── mock_cdp.py          # Mock CDP 连接
│   │   └── mock_llm.py          # Mock LLM
│   └── test_data/
│       ├── ssh_responses/        # 模拟 SSH 输出
│       ├── cdp_responses/        # 模拟 CDP 响应
│       └── sample_bugs/          # 模拟 Bug 场景
├── test_ssh_tool.py
├── test_cdp_tool.py
├── test_log_parser.py
├── test_code_search.py
├── test_agent.py
├── test_integration.py          # 集成测试
└── test_e2e.py                  # 端到端测试
```

### 验收标准

- [ ] SSH 工具：能连接服务器、执行命令、读取日志
- [ ] CDP 工具：能连接浏览器、截图、获取 Console 和 Network 日志
- [ ] Agent：能并行调用工具，生成诊断报告
- [ ] 单元测试覆盖率 > 80%
- [ ] 集成测试全部通过
- [ ] E2E 测试至少 3 个场景通过
- [ ] CLI 可正常运行
- [ ] 诊断耗时 < 3 分钟（典型场景）

---

## Phase 3: 产品级 Agent (TBD)

### 目标

掌握 Agent 架构设计和产品化能力。

### 方向选择（Phase 2 完成后决定）

| 方向 | 学习价值 | 商业价值 | 难度 |
|------|---------|---------|------|
| **多 Agent 协作** | 高（架构设计） | 中 | 高 |
| **Agent + RAG** | 高（知识管理） | 高 | 中 |
| **Agent + MCP** | 高（工具生态） | 高 | 中 |
| **Agent Web UI** | 中（前端能力） | 高 | 中 |
| **Agent 部署平台** | 高（运维能力） | 高 | 高 |

### 待定内容

- 具体方向选择
- 功能范围定义
- 技术选型确认
- 任务分解
- 测试策略

---

## 跨阶段复用

### core/ 模块演进

| 模块 | Phase 1 | Phase 2 | Phase 3 |
|------|---------|---------|---------|
| `base_agent.py` | 基础 Agent 类 | 添加并行工具调用 | 添加 Sub-Agent 支持 |
| `base_tool.py` | 基础 Tool 类 | 添加连接管理 | 添加 MCP 适配 |
| `memory.py` | 基础记忆 | 添加会话记忆 | 添加长期记忆 |
| `planner.py` | 基础规划 | 添加多步规划 | 添加动态规划 |

### 测试基础设施演进

| 组件 | Phase 1 | Phase 2 | Phase 3 |
|------|---------|---------|---------|
| Mock LLM | 基础 mock | 添加流式 mock | 添加多模型 mock |
| Mock 工具 | 无 | SSH/CDP mock | 更多工具 mock |
| 测试数据 | 日志样本 | 服务器响应样本 | 完整场景样本 |
| CI | 手动运行 | 手动运行 | GitHub Actions |
