"""Bug Diagnoser Agent - Phase 2 of Agent Bug Killer."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.base_agent import AgentConfig, create_agent
from core.prompt_loader import load_scenario_prompt
from scenarios.bug_diagnoser.src.tools.cdp_tool import (
    cdp_connect,
    cdp_console,
    cdp_network,
    cdp_screenshot,
)
from scenarios.bug_diagnoser.src.tools.code_search import code_search
from scenarios.bug_diagnoser.src.tools.ssh_tool import ssh_exec, ssh_read_log
from scenarios.log_analyzer.src.tools.log_parser import log_parser

_DEFAULT_SYSTEM_PROMPT = """\
You are a Bug Diagnoser Agent specialized in diagnosing production issues
across multiple data sources.

Your Capabilities:
- Execute commands on remote servers via SSH (ssh_exec tool)
- Read log files from remote servers (ssh_read_log tool)
- Take screenshots and capture browser logs via CDP (cdp_screenshot, cdp_console, cdp_network tools)
- Search code for error patterns (code_search tool)
- Parse and analyze log content (log_parser tool)

Diagnostic Workflow:
1. Information Gathering (parallel when possible):
   - SSH: Check application logs, process status, port usage
   - CDP: Take screenshots, capture console errors, monitor network requests
   - Code Search: Find relevant error handling code

2. Analysis Phase:
   - Extract error keywords and patterns
   - Classify error type (JS errors, network errors, rendering issues, server crashes)
   - Correlate timestamps across sources
   - Identify code locations from stack traces

3. Diagnosis Phase:
   - Determine root cause
   - Assess impact scope
   - Generate fix recommendations

Response Format:
Always respond with a structured diagnostic report:
{
  "summary": "One-line summary",
  "error_type": "classification",
  "sources_checked": ["ssh", "cdp", "code"],
  "findings": [
    {
      "source": "ssh|cdp|code",
      "description": "What was found",
      "evidence": "Supporting data"
    }
  ],
  "root_cause": "Root cause analysis",
  "impact": "What this affects",
  "recommendations": ["Fix 1", "Fix 2"],
  "urgency": "critical|high|medium|low"
}

Rules:
1. Always check multiple sources before concluding
2. Correlate findings across SSH, CDP, and code
3. Provide evidence for every conclusion
4. Prioritize fixes by urgency
5. Handle tool failures gracefully - try alternative approaches"""

_SCENARIO_DIR = Path(__file__).resolve().parent.parent.parent
SYSTEM_PROMPT = load_scenario_prompt(_SCENARIO_DIR, default=_DEFAULT_SYSTEM_PROMPT)


def create_bug_diagnoser_agent(
    model: str = "anthropic:claude-sonnet-4-6",
    debug: bool = False,
) -> Any:
    """Create a Bug Diagnoser Agent.

    Args:
        model: The LLM model to use.
        debug: Enable debug mode.

    Returns:
        A compiled agent ready for invocation.
    """
    config = AgentConfig(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[
            ssh_exec, ssh_read_log,
            cdp_connect, cdp_screenshot, cdp_console, cdp_network,
            code_search, log_parser,
        ],
        debug=debug,
    )
    return create_agent(config)


def diagnose_bug(
    bug_description: str,
    server_info: dict | None = None,
    browser_ws: str | None = None,
    code_path: str | None = None,
    model: str = "anthropic:claude-sonnet-4-6",
    debug: bool = False,
) -> dict:
    """Diagnose a production bug using multiple data sources.

    Args:
        bug_description: Description of the bug.
        server_info: SSH connection info (host, user, key_path).
        browser_ws: CDP WebSocket URL.
        code_path: Path to source code for search.
        model: The LLM model to use.
        debug: Enable debug mode.

    Returns:
        A diagnostic report dictionary.
    """
    agent = create_bug_diagnoser_agent(model=model, debug=debug)

    context_parts = [f"Bug description: {bug_description}"]
    if server_info:
        host = server_info.get("host", "unknown")
        user = server_info.get("user", "unknown")
        context_parts.append(f"Server: {host} (user: {user})")
    if browser_ws:
        context_parts.append(f"Browser CDP: {browser_ws}")
    if code_path:
        context_parts.append(f"Code path: {code_path}")

    result = agent.invoke({
        "messages": [{"role": "user", "content": "\n".join(context_parts)}]
    })
    return result
