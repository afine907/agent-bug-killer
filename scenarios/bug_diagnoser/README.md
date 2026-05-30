# Scenario 2: Online Bug Diagnoser (Bug Diagnoser)

## Overview

Diagnose production bugs through multiple data sources (SSH server logs, browser CDP, code search) and generate a comprehensive diagnostic report.

## Features

- Execute remote commands and read logs via SSH
- CDP browser screenshots, Console logs, Network requests
- Code search to locate error handling logic
- Multi-source correlation analysis and diagnostic report generation

## Tools

| Tool | Function |
|------|------|
| `ssh_exec` | Execute remote commands via SSH |
| `ssh_read_log` | Read remote log files |
| `cdp_connect` | Connect to browser CDP |
| `cdp_screenshot` | Take browser screenshots |
| `cdp_console` | Retrieve Console logs |
| `cdp_network` | Retrieve Network requests |
| `code_search` | Search code |
| `log_parser` | Log parsing (reused from log_analyzer) |

## Usage

### CLI

```bash
# Basic diagnosis
uv run python scenarios/bug_diagnoser/cli.py \
  --bug "white screen on page" \
  --host prod-server \
  --user deploy \
  --key ~/.ssh/id_rsa

# Diagnosis with browser
uv run python scenarios/bug_diagnoser/cli.py \
  --bug "API timeout" \
  --host api-server \
  --browser ws://localhost:9222/devtools/browser/...

# Diagnosis with code search
uv run python scenarios/bug_diagnoser/cli.py \
  --bug "NPE in checkout" \
  --code /path/to/source
```

### Python API

```python
from scenarios.bug_diagnoser.src.agent import diagnose_bug

result = diagnose_bug(
    bug_description="white screen on page",
    server_info={"host": "prod-server", "user": "deploy"},
    browser_ws="ws://localhost:9222/devtools/browser/...",
    code_path="/path/to/source",
)
print(result)
```

## Prerequisites

- SSH: Requires an accessible server and key
- CDP: Requires a running Chrome instance (`chrome --remote-debugging-port=9222`)
- Code: Requires a local source code directory

## Testing

```bash
# Run unit tests
uv run pytest scenarios/bug_diagnoser/tests/ -v

# Run integration tests
uv run pytest scenarios/bug_diagnoser/tests/ -v -m integration
```
