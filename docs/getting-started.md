# Getting Started with Agent Bug Killer

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-org/agent-bug-killer.git
cd agent-bug-killer

# Install dependencies
uv sync

# Set up environment
cp .env.example .env
# Edit .env with your API keys
```

### 2. Run Your First Analysis

#### Analyze a Log File

```bash
# Using CLI
uv run python scenarios/log_analyzer/cli.py --file /path/to/error.log

# With output format
uv run python scenarios/log_analyzer/cli.py --file error.log --output report.md --format markdown
```

#### Using Python API

```python
from scenarios.log_analyzer.src.agent import analyze_log

# Analyze a log file
result = analyze_log("/path/to/error.log")
print(result)
```

### 3. Start the Web API

```bash
# Start the API server
uv run uvicorn api:app --reload

# Access the API
curl http://localhost:8000/health
```

## Core Concepts

### Agents

Agent Bug Killer uses AI agents for diagnosis:

1. **Log Analyzer Agent**: Analyzes log files for errors
2. **Bug Diagnoser Agent**: Multi-source bug diagnosis

### Tools

Agents use tools to gather information:

- **file_reader**: Read local files
- **log_parser**: Parse log entries
- **ssh_exec**: Execute remote commands
- **cdp_***: Browser debugging
- **code_search**: Search source code

### Knowledge Base

The system learns from past errors:

- Error patterns are stored
- Solutions are indexed
- Similar errors are grouped

## Examples

### Example 1: Analyze Python Traceback

```python
from scenarios.log_analyzer.src.tools.log_parser import log_parser

log_content = """
2024-01-15 10:30:15 ERROR [web.app] Request failed
Traceback (most recent call last):
  File "/app/views.py", line 42
    result = process(data)
ValueError: Invalid input
"""

entries = log_parser.invoke({"content": log_content})
for entry in entries:
    print(f"[{entry['level']}] {entry['message']}")
```

### Example 2: Search for Error Patterns

```python
from core.analyzer import analyze_error

result = analyze_error("ConnectionRefused: cannot connect to database")
print(f"Error type: {result.error_type}")
print(f"Category: {result.category}")
print(f"Suggestions: {result.fix_suggestions}")
```

### Example 3: Use Knowledge Base

```python
from core.knowledge_base import KnowledgeBase

kb = KnowledgeBase()
results = kb.search("database connection")

for entry in results:
    print(f"{entry.title}: {entry.solution}")
```

### Example 4: Generate Fix Suggestions

```python
from core.analyzer import analyze_error
from core.fix_suggestions import generate_fix_suggestions

analysis = analyze_error("OutOfMemoryError: Java heap space")
suggestions = generate_fix_suggestions(analysis)

for suggestion in suggestions:
    print(f"Fix: {suggestion.title}")
    print(f"Priority: {suggestion.priority}")
    print(f"Steps: {suggestion.steps}")
```

## Configuration

### Environment Variables

```bash
# LLM Configuration
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_MODEL=anthropic:claude-sonnet-4-6

# SSH Configuration
SSH_KEY_PATH=~/.ssh/id_rsa
SSH_DEFAULT_USER=root
SSH_TIMEOUT=30

# CDP Configuration
CDP_BROWSER_WS=ws://localhost:9222/devtools/browser/...
CDP_TIMEOUT=10

# Logging
LOG_LEVEL=INFO
```

### Settings File

```python
from core.settings import settings

# Access settings
print(settings.llm_model)
print(settings.ssh_timeout)
print(settings.cdp_timeout)
```

## CLI Reference

### Log Analyzer

```bash
uv run python scenarios/log_analyzer/cli.py [OPTIONS]

Options:
  --file, -f PATH     Path to log file
  --text, -t TEXT     Raw log text
  --model, -m TEXT    LLM model
  --output, -o PATH   Output file
  --format TEXT       Output format (json, markdown, html)
  --debug             Enable debug mode
```

### Bug Diagnoser

```bash
uv run python scenarios/bug_diagnoser/cli.py [OPTIONS]

Options:
  --bug TEXT          Bug description (required)
  --host TEXT         SSH server host
  --user TEXT         SSH username
  --key PATH          SSH key path
  --browser TEXT      CDP WebSocket URL
  --code PATH         Source code path
  --model, -m TEXT    LLM model
  --output, -o PATH   Output file
  --debug             Enable debug mode
```

## API Reference

See [API Reference](./api-reference.md) for complete API documentation.

## Troubleshooting

### Common Issues

#### 1. API Key Not Found

```
Error: ANTHROPIC_API_KEY not set
```

**Solution**: Set your API key in `.env` file.

#### 2. SSH Connection Failed

```
Error: Authentication failed
```

**Solution**: Check SSH key path and permissions.

#### 3. CDP Connection Failed

```
Error: Connection refused
```

**Solution**: Start Chrome with `--remote-debugging-port=9222`.

### Getting Help

- GitHub Issues: Report bugs
- Discussions: Ask questions
- Documentation: Read docs

## Next Steps

1. Read the [Architecture Guide](./architecture-v2.md)
2. Explore the [API Reference](./api-reference.md)
3. Check the [Competitor Analysis](./competitor-analysis.md)
4. Review the [Roadmap](./roadmap-v2.md)
