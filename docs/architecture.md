# Architecture

> Agent Bug Killer — System Architecture and Design

## Table of Contents

- [System Overview](#system-overview)
- [Layer Architecture](#layer-architecture)
- [Module Map](#module-map)
- [Data Flow: Log Analysis](#data-flow-log-analysis)
- [Data Flow: Bug Diagnosis](#data-flow-bug-diagnosis)
- [Data Flow: RCA Pipeline](#data-flow-rca-pipeline)
- [Core Module Dependencies](#core-module-dependencies)
- [API Architecture](#api-architecture)
- [Agent Architecture](#agent-architecture)
- [Deployment Architecture](#deployment-architecture)
- [Technology Stack](#technology-stack)

---

## System Overview

```mermaid
graph TB
    subgraph "User Interfaces"
        CLI["CLI<br/>scenarios/*/cli.py"]
        SDK["Python SDK<br/>import agents directly"]
        API["REST API<br/>FastAPI :8000"]
    end

    subgraph "Agent Layer"
        LA["LogAnalyzerAgent"]
        BD["BugDiagnoserAgent"]
    end

    subgraph "Core Engine"
        RCA["RCA Engine"]
        EG["Error Groups"]
        AN["Analyzer"]
        KB["Knowledge Base"]
        FS["Fix Suggestions"]
        MT["Metrics"]
    end

    subgraph "Tool Layer"
        FR["file_reader"]
        LP["log_parser"]
        SSH["ssh_exec / ssh_read_log"]
        CDP["cdp_connect / cdp_screenshot / cdp_console / cdp_network"]
        CS["code_search"]
    end

    subgraph "Infrastructure"
        CFG["Settings"]
        HD["History"]
        CH["Cache"]
        RT["Retry"]
        VL["Validators"]
        PG["Progress"]
        EX["Exceptions"]
        PL["Prompt Loader"]
        MM["Memory"]
    end

    subgraph "External Services"
        LLM["Claude API<br/>(via LangChain)"]
        SRV["Remote Servers<br/>(SSH/Paramiko)"]
        BRW["Browsers<br/>(CDP/WebSocket)"]
    end

    CLI --> LA & BD
    SDK --> LA & BD
    API --> LA & BD

    LA --> FR & LP
    BD --> SSH & CDP & CS & LP

    LA & BD --> RCA
    RCA --> EG & AN & KB
    AN --> FS

    SSH --> SRV
    CDP --> BRW
    LA & BD --> LLM

    LA & BD -.-> CFG & HD & CH & RT & VL & PG & EX & PL & MM
```

---

## Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1: User Interfaces                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────────────┐  │
│  │   CLI    │  │  Python  │  │      REST API (FastAPI)       │  │
│  │ Click +  │  │   SDK    │  │                               │  │
│  │  Rich    │  │          │  │  Middleware:                   │  │
│  │          │  │          │  │  ├─ RequestLogging             │  │
│  │          │  │          │  │  └─ RateLimit (60 req/min)     │  │
│  └──────────┘  └──────────┘  └──────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  Layer 2: Agent Layer                                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  LogAnalyzerAgent          BugDiagnoserAgent              │   │
│  │  ├─ file_reader            ├─ ssh_exec / ssh_read_log     │   │
│  │  └─ log_parser             ├─ cdp_* (4 tools)             │   │
│  │                            ├─ code_search                 │   │
│  │                            └─ log_parser (shared)         │   │
│  │  Built on: LangChain DeepAgents + LangGraph               │   │
│  └──────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  Layer 3: Core Engine                                            │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐   │
│  │ RCA Engine  │  │  Analyzer   │  │   Knowledge Base     │   │
│  │ 9-step      │  │  7 error    │  │   JSON-backed        │   │
│  │ analysis    │  │  patterns   │  │   search + category  │   │
│  └──────┬──────┘  └──────┬──────┘  └──────────────────────┘   │
│         │                │                                      │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────────────────────┐   │
│  │Error Groups │  │    Fix      │  │      Metrics         │   │
│  │Fingerprint +│  │ Suggestions │  │  Counter/Gauge/      │   │
│  │Aggregation  │  │             │  │  Histogram           │   │
│  └─────────────┘  └─────────────┘  └──────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  Layer 4: Infrastructure                                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│  │Settings │ │History  │ │ Cache   │ │ Retry   │ │Validators│ │
│  │.env     │ │File-    │ │File-    │ │Exponent │ │Path     │ │
│  │based    │ │based    │ │based    │ │backoff  │ │Host/Port│ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────────┐ │
│  │Progress │ │Exception│ │Prompt   │ │      Memory         │ │
│  │Tracker +│ │Hierarchy│ │Loader   │ │  DeepAgents wrapper │ │
│  │Spinner  │ │         │ │Markdown │ │                     │ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Module Map

### Core Modules

```mermaid
graph LR
    subgraph "Agent"
        BA[base_agent.py<br/>AgentConfig<br/>create_agent]
        BT[base_tool.py<br/>create_tool<br/>tool_metadata]
    end

    subgraph "Analysis"
        AN[analyzer.py<br/>ErrorPattern<br/>analyze_error]
        EG[error_groups.py<br/>ErrorGroup<br/>group_errors]
        RCA[rca_engine.py<br/>RCAResult<br/>RCAEngine]
    end

    subgraph "Intelligence"
        KB[knowledge_base.py<br/>KnowledgeEntry<br/>KnowledgeBase]
        FS[fix_suggestions.py<br/>FixSuggestion<br/>generate_fix_suggestions]
    end

    subgraph "Output"
        FM[formatters.py<br/>format_json<br/>format_markdown<br/>format_html]
        HD[history.py<br/>DiagnosticHistory<br/>save/load/search]
    end

    subgraph "Infrastructure"
        CFG[settings.py<br/>Settings]
        PL[prompt_loader.py<br/>load_prompt<br/>load_scenario_prompt]
        MM[memory.py<br/>create_memory_config]
        PP[planner.py<br/>create_diagnostic_plan]
        MT[metrics.py<br/>MetricsCollector<br/>MetricNames]
        CH[cache.py<br/>FileCache<br/>cached]
        RT[retry.py<br/>retry<br/>retry_async]
        VL[validators.py<br/>validate_*]
        PG[progress.py<br/>ProgressTracker]
        EX[exceptions.py<br/>AgentBugKillerError]
    end

    RCA --> AN & EG & KB
    FS --> AN
    BA --> CFG
```

### Scenario Modules

```mermaid
graph TB
    subgraph "log_analyzer"
        LA_AGENT[agent.py<br/>analyze_log]
        LA_FR[file_reader.py]
        LA_LP[log_parser.py]
        LA_CLI[cli.py]
        LA_PROMPT[prompts/system.md]
    end

    subgraph "bug_diagnoser"
        BD_AGENT[agent.py<br/>diagnose_bug]
        BD_SSH[ssh_tool.py<br/>ssh_exec<br/>ssh_read_log]
        BD_CDP[cdp_tool.py<br/>cdp_connect<br/>cdp_screenshot<br/>cdp_console<br/>cdp_network]
        BD_CS[code_search.py]
        BD_CLI[cli.py]
        BD_PROMPT[prompts/diagnose.md]
    end

    LA_AGENT --> LA_FR & LA_LP & LA_PROMPT
    LA_CLI --> LA_AGENT

    BD_AGENT --> BD_SSH & BD_CDP & BD_CS & LA_LP & BD_PROMPT
    BD_CLI --> BD_AGENT

    LA_AGENT & BD_AGENT --> |"via"| CORE[core/base_agent.py]
```

---

## Data Flow: Log Analysis

```mermaid
sequenceDiagram
    actor User
    participant CLI as CLI / API / SDK
    participant Agent as LogAnalyzerAgent
    participant LLM as Claude API
    participant FR as file_reader
    participant LP as log_parser
    participant RCA as RCA Engine
    participant KB as Knowledge Base
    participant FS as Fix Suggestions
    participant FM as Formatters

    User->>CLI: --file error.log
    CLI->>Agent: invoke("Analyze this log")
    Agent->>LLM: system prompt + user message

    LLM->>Agent: tool_call: file_reader(path)
    Agent->>FR: read file
    FR-->>Agent: file content

    LLM->>Agent: tool_call: log_parser(content)
    Agent->>LP: parse log
    LP-->>Agent: structured errors

    Agent->>LLM: tool results
    LLM->>Agent: diagnostic analysis

    Agent->>RCA: analyze errors
    RCA->>RCA: group_errors → fingerprint
    RCA->>RCA: analyze each group
    RCA->>KB: search known patterns
    KB-->>RCA: matching entries
    RCA-->>Agent: RCAResult (root_cause, confidence, evidence)

    Agent->>FS: generate suggestions
    FS-->>Agent: FixSuggestion list

    Agent->>FM: format report
    FM-->>CLI: JSON / Markdown / HTML
    CLI-->>User: Diagnostic Report
```

---

## Data Flow: Bug Diagnosis

```mermaid
sequenceDiagram
    actor User
    participant CLI as CLI / API
    participant Agent as BugDiagnoserAgent
    participant LLM as Claude API
    participant SSH as SSH Tools
    participant CDP as CDP Tools
    participant CS as Code Search
    participant RCA as RCA Engine
    participant Output as Formatters

    User->>CLI: --bug "blank page" --host prod
    CLI->>Agent: invoke(diagnosis context)
    Agent->>LLM: system prompt + context

    par Parallel Data Collection
        LLM->>Agent: ssh_exec("tail -100 /var/log/app.log")
        Agent->>SSH: execute command
        SSH-->>Agent: log output

        LLM->>Agent: cdp_screenshot()
        Agent->>CDP: capture screenshot
        CDP-->>Agent: screenshot path

        LLM->>Agent: cdp_console()
        Agent->>CDP: get console logs
        CDP-->>Agent: JS errors

        LLM->>Agent: code_search("error_handler")
        Agent->>CS: search source
        CS-->>Agent: code matches
    end

    Agent->>LLM: all collected data
    LLM->>Agent: analysis + findings

    Agent->>RCA: correlate errors
    RCA-->>Agent: root cause + confidence

    Agent->>Output: format report
    Output-->>CLI: structured diagnosis
    CLI-->>User: Diagnostic Report
```

---

## Data Flow: RCA Pipeline

```mermaid
flowchart TD
    A[Raw Errors] --> B[Error Grouping]
    B --> B1[normalize messages<br/>remove timestamps, UUIDs, paths]
    B1 --> B2[compute fingerprint<br/>MD5 hash]
    B2 --> B3[group by fingerprint<br/>ErrorGroup objects]

    B3 --> C[Pattern Analysis]
    C --> C1[match against 7 patterns:<br/>Connection, Timeout, OOM,<br/>NullPointer, Permission,<br/>DiskFull, Database]
    C1 --> C2[calculate severity<br/>critical/high/medium/low]

    C2 --> D[Knowledge Lookup]
    D --> D1[search knowledge base<br/>by pattern + category]
    D1 --> D2[match against known<br/>error patterns + tags]

    D2 --> E[Root Cause Determination]
    E --> E1[determine category<br/>network/memory/auth/...]
    E1 --> E2[generate root cause<br/>description]
    E2 --> E3[calculate confidence<br/>0.0 - 1.0]

    E3 --> E4[collect evidence<br/>error messages + stack traces]

    E4 --> F[Fix Generation]
    F --> F1[generate fix suggestions<br/>with steps + code examples]
    F1 --> F2[prioritize by<br/>impact + effort]

    F2 --> G[RCAResult]
    G --> G1[root_cause]
    G --> G2[confidence]
    G --> G3[category + severity]
    G --> G4[evidence list]
    G --> G5[fix_suggestions]
```

---

## Core Module Dependencies

```mermaid
graph TD
    settings --> base_agent & base_tool
    prompt_loader --> |"loads .md files"| base_agent
    memory --> |"wraps DeepAgents"| base_agent

    base_agent --> |"uses"| deepagents[deepagents library]
    base_tool --> |"uses"| langchain[langchain-core]

    analyzer --> fix_suggestions
    error_groups --> rca_engine
    analyzer --> rca_engine
    knowledge_base --> rca_engine

    settings --> |"env config"| scenarios[scenarios/*]
    base_agent --> scenarios
    prompt_loader --> scenarios

    subgraph "Zero Dependencies (standalone)"
        formatters
        history
        cache
        retry
        validators
        progress
        exceptions
        metrics
    end

    style deepagents fill:#e1f5fe
    style langchain fill:#e1f5fe
```

---

## API Architecture

```mermaid
graph TB
    subgraph "FastAPI Application"
        APP[api/__init__.py<br/>app: FastAPI]

        subgraph "Middleware Stack"
            ML[RequestLoggingMiddleware<br/>method, path, status, duration]
            RL[RateLimitMiddleware<br/>60 req/min per IP]
        end

        subgraph "Routes /api/v1"
            R1[POST /analyze-log<br/>log_analyzer.py]
            R2[POST /diagnose<br/>bug_diagnoser.py]
            R3[GET/DELETE /history<br/>history.py]
            R4[GET /knowledge<br/>knowledge.py]
        end

        HEALTH[GET /health]
    end

    APP --> ML --> RL --> R1 & R2 & R3 & R4
    APP --> HEALTH

    R1 --> |"uses"| FR2[file_reader + log_parser]
    R2 --> |"placeholder"| BD2[BugDiagnoserAgent]
    R3 --> |"uses"| HD2[DiagnosticHistory]
    R4 --> |"uses"| KB2[KnowledgeBase]
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check + version |
| `/api/v1/analyze-log` | POST | Analyze log file or text |
| `/api/v1/diagnose` | POST | Diagnose production bug |
| `/api/v1/history` | GET | List diagnostic reports |
| `/api/v1/history/{id}` | GET | Get specific report |
| `/api/v1/history/{id}` | DELETE | Delete report |
| `/api/v1/history/search/{q}` | GET | Search reports |
| `/api/v1/knowledge` | GET | List knowledge entries |
| `/api/v1/knowledge/{id}` | GET | Get specific entry |
| `/api/v1/knowledge/search/{q}` | GET | Search knowledge base |

---

## Agent Architecture

```mermaid
graph TB
    subgraph "Agent Creation Flow"
        CONFIG[AgentConfig<br/>model, system_prompt,<br/>tools, middleware]
        FACTORY[create_agent<br/>base_agent.py]
        AGENT[Compiled LangGraph Agent]
    end

    CONFIG --> FACTORY --> AGENT

    subgraph "DeepAgents Capabilities"
        PLN[Planning<br/>auto task decomposition]
        MEM[Memory<br/>cross-session context]
        SUB[Sub-agents<br/>delegate to specialists]
        MW[Middleware<br/>logging, retry, auth]
        HITL[Human-in-the-loop<br/>sensitive operation approval]
    end

    AGENT --> PLN & MEM & SUB & MW & HITL

    subgraph "LLM Integration"
        CLAUDE[ChatAnthropic<br/>claude-sonnet-4-6]
        HAIKU[ChatAnthropic<br/>claude-haiku-4-5]
    end

    AGENT --> |"primary"| CLAUDE
    AGENT --> |"fallback"| HAIKU
```

### Agent Lifecycle

```
1. User Input ─→ 2. Agent receives message
                       ↓
                  3. LLM decides action
                       ↓
              ┌─── 4a. Tool Call ──→ Execute tool ──→ Return result ──┐
              │                                                        │
              └─── 4b. Final Answer ──→ Return to user                 │
                                                                       │
                  5. Loop back to step 3 until done ◄──────────────────┘
```

---

## Deployment Architecture

```mermaid
graph TB
    subgraph "Docker Container"
        subgraph "Application"
            UVICORN[uvicorn<br/>ASGI server]
            FASTAPI[FastAPI app]
            AGENTS[Agent instances]
        end

        subgraph "Storage"
            DIAG[".diagnostics/<br/>Report history"]
            CACHE[".cache/<br/>File cache"]
            KB_FILE["knowledge_base.json"]
        end
    end

    subgraph "External"
        ANTHROPIC_API["Anthropic API<br/>(Claude)"]
        REMOTE["Remote Servers<br/>(SSH)"]
        BROWSER["Browsers<br/>(CDP)"]
    end

    subgraph "CI/CD"
        GHA["GitHub Actions"]
        PYTEST["pytest + ruff + mypy"]
    end

    UVICORN --> FASTAPI --> AGENTS
    AGENTS --> DIAG & CACHE & KB_FILE
    AGENTS --> ANTHROPIC_API & REMOTE & BROWSER
    GHA --> PYTEST
```

### Docker

```bash
# Build
docker build -t agent-bug-killer .

# Run
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  agent-bug-killer
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Agent Framework** | LangChain DeepAgents | Agent creation, planning, tool orchestration |
| **Runtime** | LangGraph | State management, streaming, persistence |
| **LLM** | Claude API (via langchain-anthropic) | Natural language understanding + tool use |
| **API** | FastAPI + uvicorn | RESTful API server |
| **SSH** | Paramiko | Remote server command execution |
| **Browser** | websockets | Chrome DevTools Protocol |
| **CLI** | Click + Rich | Command-line interface |
| **Config** | pydantic-settings | Environment-based configuration |
| **Testing** | pytest + pytest-asyncio + pytest-cov | Unit + integration + coverage |
| **Linting** | ruff | Code style + import sorting |
| **Type Check** | mypy (strict) | Static type analysis |
| **Build** | hatchling + uv | Package management |
| **Container** | Docker | Deployment |

---

## Design Principles

1. **Modularity** — Each module is independent and testable in isolation
2. **Extensibility** — New tools, agents, and analyzers can be added without modifying existing code
3. **Layer Separation** — Agents depend on Core, Core is framework-agnostic, Infrastructure has zero agent dependencies
4. **Fail-Safe** — Retry logic, input validation, structured exceptions, graceful degradation
5. **Observability** — Metrics collection, request logging, progress tracking
6. **Convention over Configuration** — Sensible defaults, override via environment variables
