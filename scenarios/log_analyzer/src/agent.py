"""Log Analyzer Agent - Phase 1 of Agent Bug Killer."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.base_agent import AgentConfig, create_agent
from scenarios.log_analyzer.src.tools.file_reader import file_reader
from scenarios.log_analyzer.src.tools.log_parser import log_parser

SYSTEM_PROMPT = """You are a Log Analyzer Agent specialized in diagnosing application errors from log files.

Your Capabilities:
- Read log files from disk using the file_reader tool
- Parse and extract error information using the log_parser tool
- Analyze error patterns and provide structured diagnostic reports

Response Format:
Always respond with a JSON diagnostic report containing:
{
  "summary": "One-line summary of the diagnosis",
  "errors": [
    {
      "level": "ERROR",
      "type": "exception_type",
      "message": "Error message",
      "location": "file:line or module",
      "stack_trace": "relevant stack trace"
    }
  ],
  "root_cause": "Analysis of the root cause",
  "impact": "What this error affects",
  "recommendations": ["Fix suggestion 1", "Fix suggestion 2"]
}

Analysis Rules:
1. Focus on ERROR and CRITICAL level entries
2. Extract exception types and their messages
3. Identify the source file and line number from stack traces
4. Look for patterns across multiple errors
5. Correlate timestamps to understand error sequences
6. Provide actionable recommendations for each error"""


def create_log_analyzer_agent(
    model: str = "anthropic:claude-sonnet-4-6",
    debug: bool = False,
) -> Any:
    """Create a Log Analyzer Agent.

    Args:
        model: The LLM model to use.
        debug: Enable debug mode.

    Returns:
        A compiled agent ready for invocation.
    """
    config = AgentConfig(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[file_reader, log_parser],
        debug=debug,
    )
    return create_agent(config)


def analyze_log(
    log_path: str | Path,
    model: str = "anthropic:claude-sonnet-4-6",
    debug: bool = False,
) -> dict:
    """Analyze a log file and return a diagnostic report.

    Args:
        log_path: Path to the log file to analyze.
        model: The LLM model to use.
        debug: Enable debug mode.

    Returns:
        A diagnostic report dictionary.
    """
    agent = create_log_analyzer_agent(model=model, debug=debug)
    result = agent.invoke({
        "messages": [{"role": "user", "content": f"Analyze the log file at: {log_path}"}]
    })
    return result
