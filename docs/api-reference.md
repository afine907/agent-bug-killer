# API Reference

## Web API Endpoints

### Health Check

```
GET /health
```

Returns server health status.

**Response:**
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

### Log Analysis

```
POST /api/v1/analyze-log
```

Analyze a log file or text for errors.

**Request Body:**
```json
{
  "file_path": "/path/to/log/file",
  "log_text": "raw log text",
  "model": "anthropic:claude-sonnet-4-6"
}
```

**Response:**
```json
{
  "total_errors": 2,
  "errors": [
    {
      "level": "ERROR",
      "message": "Connection refused",
      "timestamp": "2024-01-15 10:00:00",
      "source": "db.connection",
      "stack_trace": "..."
    }
  ],
  "summary": "Found 2 error(s)"
}
```

### Bug Diagnosis

```
POST /api/v1/diagnose
```

Diagnose a production bug using multiple data sources.

**Request Body:**
```json
{
  "bug_description": "Page shows 500 error",
  "server_host": "prod-server",
  "server_user": "deploy",
  "browser_ws": "ws://localhost:9222/devtools/browser/...",
  "code_path": "/path/to/source"
}
```

**Response:**
```json
{
  "summary": "Database connection pool exhausted",
  "error_type": "database",
  "findings": [
    {
      "source": "ssh",
      "description": "Connection pool at 100% capacity",
      "evidence": "2024-01-15 ERROR db.pool Pool exhausted"
    }
  ],
  "root_cause": "Connection pool size too small",
  "recommendations": ["Increase pool size to 20"],
  "urgency": "high"
}
```

### History

```
GET /api/v1/history
```

List diagnostic history entries.

**Query Parameters:**
- `limit` (int, default: 20): Maximum entries to return
- `offset` (int, default: 0): Number of entries to skip

**Response:**
```json
{
  "total": 10,
  "entries": [
    {
      "id": "abc123",
      "timestamp": "2024-01-15T10:00:00",
      "summary": "Database connection failed",
      "metadata": {}
    }
  ]
}
```

```
GET /api/v1/history/{report_id}
```

Get a specific diagnostic report.

```
DELETE /api/v1/history/{report_id}
```

Delete a diagnostic report.

```
GET /api/v1/history/search/{query}
```

Search diagnostic history.

### Knowledge Base

```
GET /api/v1/knowledge
```

List knowledge base entries.

**Query Parameters:**
- `category` (string, optional): Filter by category
- `limit` (int, default: 20): Maximum entries to return

```
GET /api/v1/knowledge/search/{query}
```

Search knowledge base.

```
GET /api/v1/knowledge/{entry_id}
```

Get a specific knowledge entry.

## CLI Commands

### Log Analyzer

```bash
uv run python scenarios/log_analyzer/cli.py [OPTIONS]
```

**Options:**
- `--file, -f PATH`: Path to log file
- `--text, -t TEXT`: Raw log text
- `--model, -m TEXT`: LLM model (default: anthropic:claude-sonnet-4-6)
- `--output, -o PATH`: Output file path
- `--format TEXT`: Output format (json, markdown, html)
- `--debug`: Enable debug mode

### Bug Diagnoser

```bash
uv run python scenarios/bug_diagnoser/cli.py [OPTIONS]
```

**Options:**
- `--bug TEXT`: Bug description (required)
- `--host TEXT`: SSH server host
- `--user TEXT`: SSH username
- `--key PATH`: SSH key path
- `--browser TEXT`: CDP WebSocket URL
- `--code PATH`: Source code path
- `--model, -m TEXT`: LLM model
- `--output, -o PATH`: Output file path
- `--debug`: Enable debug mode

## Python API

### Log Analyzer

```python
from scenarios.log_analyzer.src.agent import analyze_log

result = analyze_log("/path/to/error.log")
print(result)
```

### Bug Diagnoser

```python
from scenarios.bug_diagnoser.src.agent import diagnose_bug

result = diagnose_bug(
    bug_description="Page shows 500 error",
    server_info={"host": "prod-server", "user": "deploy"},
    browser_ws="ws://localhost:9222/devtools/browser/...",
    code_path="/path/to/source",
)
print(result)
```

### Core Modules

```python
# Error Analysis
from core.analyzer import analyze_error
result = analyze_error("ConnectionRefused: cannot connect")

# Knowledge Base
from core.knowledge_base import KnowledgeBase
kb = KnowledgeBase()
entries = kb.search("database")

# Fix Suggestions
from core.fix_suggestions import generate_fix_suggestions
suggestions = generate_fix_suggestions(analysis_result)

# Report Formatting
from core.formatters import format_report
report = format_report(data, fmt="markdown")

# Diagnostic History
from core.history import DiagnosticHistory
history = DiagnosticHistory()
history.save(report, metadata={"bug": "description"})
```
