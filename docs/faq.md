# Frequently Asked Questions (FAQ)

## General

### What is Agent Bug Killer?

Agent Bug Killer is an AI-powered bug diagnosis system that helps developers
identify and fix production issues faster. It uses multiple data sources
(logs, server, browser, code) to provide intelligent diagnostics.

### How does it work?

1. **Collect**: Gathers data from multiple sources (SSH, CDP, logs, code)
2. **Analyze**: Uses AI to identify error patterns
3. **Diagnose**: Performs root cause analysis
4. **Suggest**: Provides fix recommendations

### Is it free?

Yes! Agent Bug Killer is open source under the MIT license.
You only need an API key for the LLM (Claude).

### What LLMs are supported?

Currently supports:
- Claude (Anthropic) - Recommended
- Other models via LangChain

## Installation

### What are the system requirements?

- Python 3.12+
- uv package manager
- 2GB+ RAM
- Internet connection (for LLM API)

### How do I install it?

```bash
git clone https://github.com/afine907/agent-bug-killer.git
cd agent-bug-killer
uv sync
cp .env.example .env
# Edit .env with your API key
```

### Do I need Docker?

No, Docker is optional. You can run directly with Python.
Docker is recommended for production deployment.

## Usage

### How do I analyze a log file?

```bash
uv run python scenarios/log_analyzer/cli.py --file /path/to/error.log
```

### How do I diagnose a bug?

```bash
uv run python scenarios/bug_diagnoser/cli.py \
  --bug "Description of the bug" \
  --host server-host \
  --user deploy
```

### Can I use it without SSH access?

Yes! You can:
- Analyze local log files
- Use the web API
- Use the Python API directly

### How accurate is the diagnosis?

Accuracy depends on:
- Quality of input data
- Similarity to known patterns
- Completeness of context

Typical accuracy: 70-90% for known error patterns.

### Can I add my own error patterns?

Yes! Add entries to the knowledge base:

```python
from core.knowledge_base import KnowledgeBase, KnowledgeEntry

kb = KnowledgeBase()
kb.add_entry(KnowledgeEntry(
    id="custom-001",
    title="My Custom Error",
    error_pattern="...",
    category="custom",
    root_cause="...",
    solution="...",
))
```

## API

### How do I start the API server?

```bash
uv run uvicorn api:app --host 0.0.0.0 --port 8000
```

### What endpoints are available?

- `GET /health` - Health check
- `POST /api/v1/analyze-log` - Log analysis
- `POST /api/v1/diagnose` - Bug diagnosis
- `GET /api/v1/history` - Diagnostic history
- `GET /api/v1/knowledge` - Knowledge base

### Is there rate limiting?

Yes, default is 60 requests per minute per IP.

### Do I need authentication?

Currently no, but API key authentication is planned.

## Troubleshooting

### I get "API key not found"

Set your API key in `.env`:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### SSH connection fails

Check:
1. SSH key path is correct
2. Key has proper permissions (`chmod 600`)
3. Server is reachable
4. User has access

### CDP connection fails

Check:
1. Chrome is running with `--remote-debugging-port=9222`
2. Port is accessible
3. WebSocket URL is correct

### Tests fail

```bash
# Run with verbose output
uv run pytest -v

# Run specific test
uv run pytest path/to/test.py::test_name -v
```

## Contributing

### How can I contribute?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

### Where do I report bugs?

Use [GitHub Issues](https://github.com/afine907/agent-bug-killer/issues)

### Where do I ask questions?

Use [GitHub Discussions](https://github.com/afine907/agent-bug-killer/discussions)

## Roadmap

### What's next?

See [Roadmap V2](./roadmap-v2.md) for planned features:

- v0.3.0: Production readiness
- v0.4.0: Advanced features
- v0.5.0: Ecosystem

### Will there be a cloud version?

Yes, a hosted version is planned for v0.5.0.

### Will there be more integrations?

Yes, planned integrations include:
- GitHub Issues
- Slack
- PagerDuty
- Jira
