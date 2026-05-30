# Scenario 1: Log Analyzer

## Overview

Extract error information from log files, analyze error patterns, and generate structured diagnostic reports.

## Features

- Read local log files (with support for multiple encodings)
- Parse standard log formats (timestamp, level, module, message)
- Extract Python Traceback and stack trace information
- Generate diagnostic reports in JSON format

## Tools

| Tool | Description |
|------|-------------|
| `file_reader` | Read file content with encoding fallback and size limits |
| `log_parser` | Parse logs to extract structured error information |

## Usage

### CLI

```bash
# Analyze a log file
uv run python scenarios/log_analyzer/cli.py --file /path/to/error.log

# Pass log text directly
uv run python scenarios/log_analyzer/cli.py --text "2024-01-15 ERROR Something failed"

# Specify output format
uv run python scenarios/log_analyzer/cli.py --file app.log --output json

# Debug mode
uv run python scenarios/log_analyzer/cli.py --file app.log --debug
```

### Python API

```python
from scenarios.log_analyzer.src.agent import analyze_log

result = analyze_log("/path/to/error.log")
print(result)
```

## Testing

```bash
# Run unit tests
uv run pytest scenarios/log_analyzer/tests/ -v

# Run integration tests
uv run pytest scenarios/log_analyzer/tests/ -v -m integration
```
