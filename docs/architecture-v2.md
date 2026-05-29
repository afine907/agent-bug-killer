# Architecture V2 — Agent Bug Killer

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      Agent Bug Killer                            │
├─────────────────────────────────────────────────────────────────┤
│  API Layer (FastAPI)                                            │
│  ├── /api/v1/analyze-log    ─ Log Analysis                      │
│  ├── /api/v1/diagnose       ─ Bug Diagnosis                     │
│  ├── /api/v1/history        ─ Diagnostic History                │
│  └── /api/v1/knowledge      ─ Knowledge Base                    │
├─────────────────────────────────────────────────────────────────┤
│  Core Engine                                                    │
│  ├── RCA Engine             ─ Root Cause Analysis               │
│  ├── Error Groups           ─ Error Aggregation                 │
│  ├── Analyzer               ─ Error Pattern Matching            │
│  ├── Knowledge Base         ─ Known Issues Database             │
│  └── Fix Suggestions        ─ Repair Recommendations            │
├─────────────────────────────────────────────────────────────────┤
│  Agent Layer                                                    │
│  ├── Log Analyzer Agent     ─ Log File Analysis                 │
│  └── Bug Diagnoser Agent    ─ Multi-Source Diagnosis            │
├─────────────────────────────────────────────────────────────────┤
│  Tool Layer                                                     │
│  ├── file_reader            ─ Local File Access                 │
│  ├── log_parser             ─ Log Parsing                       │
│  ├── ssh_exec/ssh_read_log  ─ Remote Server Access              │
│  ├── cdp_*                  ─ Browser Debugging                 │
│  └── code_search            ─ Source Code Search                │
├─────────────────────────────────────────────────────────────────┤
│  Infrastructure                                                 │
│  ├── Settings               ─ Configuration                     │
│  ├── History                ─ Diagnostic Storage                │
│  ├── Cache                  ─ Response Caching                  │
│  ├── Retry                  ─ Transient Failure Handling        │
│  └── Validators             ─ Input Validation                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Log Analysis Flow

```
User Input (file/text)
    ↓
Log Analyzer Agent
    ↓
file_reader → log_parser
    ↓
Error Groups → Analyzer
    ↓
RCA Engine → Knowledge Base
    ↓
Fix Suggestions
    ↓
Formatted Report (JSON/MD/HTML)
```

### Bug Diagnosis Flow

```
Bug Description + Sources
    ↓
Bug Diagnoser Agent
    ↓
┌─────────┬─────────┬─────────┐
│   SSH   │   CDP   │  Code   │
│ Tools   │ Tools   │ Search  │
└─────────┴─────────┴─────────┘
    ↓         ↓         ↓
    └─────────┴─────────┘
              ↓
      Error Correlation
              ↓
      RCA Engine
              ↓
    Knowledge Base Lookup
              ↓
      Fix Suggestions
              ↓
    Diagnostic Report
```

## Component Details

### Core Modules

| Module | Purpose | Dependencies |
|--------|---------|--------------|
| analyzer.py | Error pattern matching | None |
| error_groups.py | Error aggregation | None |
| rca_engine.py | Root cause analysis | analyzer, error_groups, knowledge_base |
| knowledge_base.py | Known issues database | None |
| fix_suggestions.py | Repair recommendations | analyzer |
| formatters.py | Output formatting | None |
| history.py | Diagnostic storage | None |
| cache.py | Response caching | None |
| retry.py | Transient failure handling | None |
| validators.py | Input validation | None |
| progress.py | Progress tracking | None |
| exceptions.py | Custom exceptions | None |

### Agent Modules

| Agent | Tools | Purpose |
|-------|-------|---------|
| LogAnalyzerAgent | file_reader, log_parser | Analyze log files |
| BugDiagnoserAgent | ssh_*, cdp_*, code_search, log_parser | Multi-source diagnosis |

### API Routes

| Route | Method | Purpose |
|-------|--------|---------|
| /health | GET | Health check |
| /api/v1/analyze-log | POST | Log analysis |
| /api/v1/diagnose | POST | Bug diagnosis |
| /api/v1/history | GET | List history |
| /api/v1/history/{id} | GET | Get report |
| /api/v1/history/{id} | DELETE | Delete report |
| /api/v1/history/search/{q} | GET | Search history |
| /api/v1/knowledge | GET | List knowledge |
| /api/v1/knowledge/{id} | GET | Get entry |
| /api/v1/knowledge/search/{q} | GET | Search knowledge |

## Design Principles

### 1. Modularity
Each component is independent and replaceable.

### 2. Extensibility
New tools, agents, and analyzers can be added easily.

### 3. Testability
All components are unit testable with mocks.

### 4. Performance
Caching and retry logic for production use.

### 5. Observability
Logging, metrics, and progress tracking.

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Framework | LangChain DeepAgents | Agent orchestration |
| LLM | Claude API | AI capabilities |
| API | FastAPI | Web API |
| Storage | JSON files | History and knowledge |
| Testing | pytest | Test framework |
| Linting | ruff | Code quality |
| Type Check | mypy | Type safety |
| Container | Docker | Deployment |

## Future Architecture

### Phase 4: Production Readiness
- PostgreSQL for storage
- Redis for caching
- Prometheus for metrics

### Phase 5: Advanced Features
- WebSocket for streaming
- Multi-agent orchestration
- Plugin system

### Phase 6: Ecosystem
- Third-party integrations
- Community contributions
- Enterprise features
