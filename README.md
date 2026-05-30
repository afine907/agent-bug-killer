# Agent Bug Killer

> AI-Powered Bug Diagnosis System — 不只监控，更要诊断

[![CI](https://github.com/afine907/agent-bug-killer/actions/workflows/ci.yml/badge.svg)](https://github.com/afine907/agent-bug-killer/actions)
[![Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen)](https://github.com/afine907/agent-bug-killer)
[![Python](https://img.shields.io/badge/python-3.12+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/mypy-strict-blue)](https://mypy-lang.org/)

Agent Bug Killer is an AI-driven bug diagnosis system that helps developers quickly identify and fix production issues. It combines multiple data sources (logs, servers, browsers, source code) with intelligent root cause analysis to deliver actionable diagnostic reports.

---

## Why Agent Bug Killer?

| Feature | Agent Bug Killer | Sentry | Datadog | LangSmith |
|---------|:---:|:---:|:---:|:---:|
| AI Root Cause Analysis | ✅ | ❌ | Partial | ❌ |
| Multi-Source Correlation | ✅ | ❌ | ✅ | ❌ |
| Fix Suggestions | ✅ | ❌ | ❌ | ❌ |
| Knowledge Base | ✅ | ❌ | ❌ | ❌ |
| Open Source | ✅ | ✅ | ❌ | ❌ |
| Self-Hosted | ✅ | ✅ | ❌ | ❌ |
| Error Grouping | ✅ | ✅ | ✅ | ❌ |
| Metrics Collection | ✅ | ❌ | ✅ | ❌ |

---

## Features

### 🤖 Intelligent Diagnosis
- **Root Cause Analysis (RCA)** — Pattern-matching engine with 7 built-in error categories
- **Advanced RCA Engine** — Multi-technique analysis with confidence scoring and evidence collection
- **Error Grouping** — Sentry-inspired error fingerprinting and aggregation
- **Knowledge Base** — Learn from past bugs, match known patterns
- **Fix Suggestions** — Actionable repair recommendations with code examples

### 🔧 Multi-Source Data Collection
- **SSH** — Remote server command execution and log retrieval
- **CDP** — Chrome DevTools Protocol for browser debugging
- **Log Parser** — Regex + LLM hybrid log analysis
- **Code Search** — Source code pattern matching

### 📊 Production Ready
- **RESTful API** — FastAPI with 12 endpoints
- **Metrics** — Counter, Gauge, Histogram with labels (Datadog-style)
- **Docker** — Containerized deployment
- **CI/CD** — GitHub Actions pipeline
- **Type Safe** — Strict mypy, 0 errors
- **Well Tested** — 284 tests, 92% coverage

### 📝 Flexible Output
- JSON, Markdown, and HTML report formats
- Diagnostic history with search
- CLI and API interfaces

---

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Installation

```bash
# Clone the repository
git clone https://github.com/afine907/agent-bug-killer.git
cd agent-bug-killer

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### CLI Usage

```bash
# Analyze a log file
uv run python scenarios/log_analyzer/cli.py --file /path/to/error.log

# Diagnose a bug
uv run python scenarios/bug_diagnoser/cli.py \
  --bug "Page shows blank screen" \
  --host prod-server \
  --user deploy

# Output as Markdown
uv run python scenarios/log_analyzer/cli.py \
  --file error.log \
  --output report.md \
  --format markdown
```

### API Usage

```bash
# Start the API server
uv run uvicorn api:app --reload

# Access interactive docs
open http://localhost:8000/docs
```

### Python SDK

```python
from scenarios.log_analyzer.src.agent import analyze_log
from scenarios.bug_diagnoser.src.agent import diagnose_bug

# Analyze logs
result = analyze_log("/path/to/error.log")

# Diagnose a bug
result = diagnose_bug(
    bug_description="Page shows blank screen",
    server_info={"host": "prod-server", "user": "deploy"},
)
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interfaces                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────────┐  │
│  │   CLI    │  │  Python  │  │    REST API (FastAPI)     │  │
│  │          │  │   SDK    │  │  /api/v1/analyze-log      │  │
│  │          │  │          │  │  /api/v1/diagnose         │  │
│  │          │  │          │  │  /api/v1/history          │  │
│  │          │  │          │  │  /api/v1/knowledge        │  │
│  └────┬─────┘  └────┬─────┘  └────────────┬─────────────┘  │
├───────┼──────────────┼─────────────────────┼────────────────┤
│       │     Agent Layer                    │                │
│  ┌────▼──────────────▼─────────────────────▼─────────────┐  │
│  │  LogAnalyzerAgent    BugDiagnoserAgent                 │  │
│  │  (LangChain DeepAgents)                               │  │
│  └────┬──────────────────────┬───────────────────────────┘  │
├───────┼──────────────────────┼──────────────────────────────┤
│       │  Core Engine         │  Tools                        │
│  ┌────▼────────────┐   ┌────▼────────────────────────────┐  │
│  │  RCA Engine     │   │  file_reader    log_parser       │  │
│  │  Error Groups   │   │  ssh_exec       cdp_*            │  │
│  │  Analyzer       │   │  code_search                    │  │
│  │  Knowledge Base │   └─────────────────────────────────┘  │
│  │  Fix Suggestions│                                        │
│  │  Metrics        │   ┌─────────────────────────────────┐  │
│  └─────────────────┘   │  Infrastructure                  │  │
│                        │  Settings  History  Cache         │  │
│                        │  Retry  Validators  Progress      │  │
│                        └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

For detailed architecture with data flows and component diagrams, see [docs/architecture.md](docs/architecture.md).

---

## Project Structure

```
agent-bug-killer/
├── core/                          # Core framework (19 modules)
│   ├── base_agent.py              # Agent factory (LangChain DeepAgents)
│   ├── base_tool.py               # Tool creation utilities
│   ├── settings.py                # Configuration (pydantic-settings)
│   ├── analyzer.py                # Error pattern matching (7 patterns)
│   ├── rca_engine.py              # Advanced RCA with confidence scoring
│   ├── error_groups.py            # Error fingerprinting & aggregation
│   ├── knowledge_base.py          # Known issues database
│   ├── fix_suggestions.py         # Actionable repair recommendations
│   ├── metrics.py                 # Counter/Gauge/Histogram collection
│   ├── formatters.py              # JSON/Markdown/HTML output
│   ├── history.py                 # Diagnostic report storage
│   ├── prompt_loader.py           # Dynamic prompt loading
│   ├── memory.py                  # Memory system wrapper
│   ├── planner.py                 # Diagnostic workflow planning
│   ├── cache.py                   # File-based caching
│   ├── retry.py                   # Retry with exponential backoff
│   ├── validators.py              # Input validation
│   ├── progress.py                # Progress tracking
│   └── exceptions.py              # Structured exception hierarchy
├── scenarios/                     # Agent scenarios
│   ├── log_analyzer/              # Log file analysis
│   └── bug_diagnoser/             # Multi-source bug diagnosis
├── api/                           # FastAPI web API
│   ├── __init__.py                # App factory + middleware
│   ├── middleware.py              # Logging & rate limiting
│   └── routes/                    # API endpoints
├── docs/                          # Documentation
├── tests/                         # Test suites (284 tests)
└── scripts/                       # Utility scripts
```

---

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=core --cov=scenarios --cov=api --cov-report=html

# Run linting
uv run ruff check .

# Run type checking
uv run mypy core/ scenarios/ api/
```

| Metric | Value |
|--------|-------|
| Tests | 284 |
| Pass Rate | 100% |
| Coverage | 92% |
| Mypy Errors | 0 |
| Ruff Errors | 0 |

---

## Documentation

| Document | Description |
|----------|-------------|
| [Getting Started](docs/getting-started.md) | Installation and first steps |
| [Architecture](docs/architecture-v2.md) | System design and data flows |
| [API Reference](docs/api-reference.md) | REST API endpoints |
| [Best Practices](docs/best-practices.md) | Usage recommendations |
| [FAQ](docs/faq.md) | Frequently asked questions |
| [Competitor Analysis](docs/competitor-analysis.md) | Comparison with Sentry, Datadog, etc. |
| [Roadmap](docs/roadmap-v2.md) | Future plans |
| [Community](docs/community.md) | Contributing and community guidelines |

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/agent-bug-killer.git
cd agent-bug-killer

# Create a feature branch
git checkout -b feature/your-feature

# Make changes, add tests, ensure everything passes
uv run pytest
uv run ruff check .
uv run mypy core/ scenarios/ api/

# Submit a PR
```

### Ways to Contribute

- 🐛 Report bugs via [Issues](https://github.com/afine907/agent-bug-killer/issues)
- 💡 Suggest features via [Discussions](https://github.com/afine907/agent-bug-killer/discussions)
- 📝 Improve documentation
- 🔧 Submit code via Pull Requests
- ⭐ Star the repo if you find it useful!

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

Built with [LangChain DeepAgents](https://github.com/langchain-ai/deepagents) and powered by [Claude](https://www.anthropic.com/claude).

---

<p align="center">
  <a href="https://github.com/afine907/agent-bug-killer/stargazers">⭐ Star</a> ·
  <a href="https://github.com/afine907/agent-bug-killer/issues">🐛 Issues</a> ·
  <a href="https://github.com/afine907/agent-bug-killer/discussions">💬 Discussions</a>
</p>
