# Agent Bug Killer - Architecture Diagram

## System Overview

```mermaid
graph TB
    subgraph "User Interface"
        CLI1["CLI: log-analyzer<br/>scenarios/log_analyzer/cli.py"]
        CLI2["CLI: bug-diagnoser<br/>scenarios/bug_diagnoser/cli.py"]
    end

    subgraph "Agent Layer"
        LA["LogAnalyzerAgent<br/>scenarios/log_analyzer/src/agent.py"]
        BD["BugDiagnoserAgent<br/>scenarios/bug_diagnoser/src/agent.py"]
    end

    subgraph "Core Framework (core/)"
        BA["base_agent.py<br/>AgentConfig + create_agent()"]
        BT["base_tool.py<br/>create_tool() + tool_metadata()"]
        CFG["settings.py<br/>Settings (pydantic-settings)"]
    end

    subgraph "LangChain DeepAgents"
        DGA["create_deep_agent()<br/>deepagents library"]
        LCM["ChatAnthropic<br/>langchain-anthropic"]
        LGRAPH["LangGraph Runtime<br/>state management"]
    end

    subgraph "Phase 1 Tools: Log Analyzer"
        FR["file_reader<br/>scenarios/log_analyzer/src/tools/file_reader.py"]
        LP["log_parser<br/>scenarios/log_analyzer/src/tools/log_parser.py"]
    end

    subgraph "Phase 2 Tools: Bug Diagnoser"
        SSH["ssh_exec / ssh_read_log<br/>scenarios/bug_diagnoser/src/tools/ssh_tool.py"]
        CDP["cdp_connect / cdp_screenshot<br/>cdp_console / cdp_network<br/>scenarios/bug_diagnoser/src/tools/cdp_tool.py"]
        CS["code_search<br/>scenarios/bug_diagnoser/src/tools/code_search.py"]
    end

    subgraph "External Services"
        ANTHROPIC["Anthropic API<br/>Claude Sonnet/Haiku"]
        SSH_SRV["Remote Servers<br/>via SSH/Paramiko"]
        BROWSER["Browser<br/>via CDP/WebSocket"]
    end

    CLI1 --> LA
    CLI2 --> BD
    LA --> BA
    BD --> BA
    BA --> DGA
    DGA --> LCM
    DGA --> LGRAPH
    LCM --> ANTHROPIC
    LA --> FR
    LA --> LP
    BD --> SSH
    BD --> CDP
    BD --> CS
    BD --> LP
    SSH --> SSH_SRV
    CDP --> BROWSER
```

## Data Flow: Log Analysis

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Agent
    participant LLM
    participant Tools

    User->>CLI: python cli.py --file error.log
    CLI->>Agent: invoke("Analyze error.log")
    Agent->>LLM: System prompt + user message
    LLM->>Agent: Tool call: file_reader("error.log")
    Agent->>Tools: file_reader.invoke()
    Tools-->>Agent: File content
    Agent->>LLM: Tool result
    LLM->>Agent: Tool call: log_parser(content)
    Agent->>Tools: log_parser.invoke()
    Tools-->>Agent: Parsed errors
    Agent->>LLM: Tool result
    LLM->>Agent: Diagnostic report (JSON)
    Agent-->>CLI: Report
    CLI-->>User: Formatted output
```

## Data Flow: Bug Diagnosis

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Agent
    participant LLM
    participant SSH
    participant CDP
    participant Code

    User->>CLI: python cli.py --bug "500 error" --host prod-server
    CLI->>Agent: invoke(diagnosis context)
    Agent->>LLM: System prompt + context

    par Parallel Information Gathering
        LLM->>Agent: ssh_exec("tail -100 /var/log/app.log")
        Agent->>SSH: SSH command
        SSH-->>Agent: Log output
        LLM->>Agent: cdp_screenshot()
        Agent->>CDP: Screenshot
        CDP-->>Agent: Screenshot path
        LLM->>Agent: code_search("error_handler")
        Agent->>Code: Search
        Code-->>Agent: Matches
    end

    LLM->>Agent: Analyze all findings
    LLM->>Agent: Diagnostic report (JSON)
    Agent-->>CLI: Report
    CLI-->>User: Formatted output
```

## Module Dependency Graph

```mermaid
graph LR
    subgraph "core/"
        settings --> base_agent
        settings --> base_tool
        base_agent --> deepagents
        base_tool --> langchain_core
    end

    subgraph "scenarios/log_analyzer/"
        file_reader --> langchain_core
        log_parser --> langchain_core
        agent --> base_agent
        agent --> file_reader
        agent --> log_parser
        cli --> agent
    end

    subgraph "scenarios/bug_diagnoser/"
        ssh_tool --> paramiko
        ssh_tool --> langchain_core
        cdp_tool --> websockets
        cdp_tool --> langchain_core
        code_search --> langchain_core
        agent --> base_agent
        agent --> ssh_tool
        agent --> cdp_tool
        agent --> code_search
        agent --> log_parser
        cli --> agent
    end
```

## Test Coverage Summary

```mermaid
pie title Test Coverage by Module
    "core/ (100%)" : 47
    "log_parser (100%)" : 45
    "code_search (92%)" : 33
    "ssh_tool (96%)" : 25
    "Agent tests (100%)" : 74
    "Other (75-90%)" : 97
    "CLIs (0% - integration tested)" : 91
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Agent Framework | LangChain DeepAgents | Agent creation, planning, tool orchestration |
| LLM | Claude API (via langchain-anthropic) | Natural language understanding and generation |
| Runtime | LangGraph | State management, streaming, persistence |
| SSH | Paramiko | Remote server command execution |
| CDP | websockets | Chrome DevTools Protocol communication |
| CLI | Click + Rich | Command-line interface with rich output |
| Testing | pytest + pytest-asyncio | Unit and integration testing |
| Config | pydantic-settings | Environment-based configuration |
| Build | hatchling + uv | Package management and building |
