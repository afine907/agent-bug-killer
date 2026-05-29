"""Integration tests for Bug Diagnoser scenario.

Tests tools working together without mocks:
- code_search + log_parser pipeline
- Multi-tool diagnostic workflow simulation
"""

from __future__ import annotations

from pathlib import Path

import pytest

from scenarios.bug_diagnoser.src.tools.code_search import code_search
from scenarios.log_analyzer.src.tools.log_parser import log_parser


@pytest.mark.integration
class TestCodeSearchToLogParser:
    """Test code_search and log_parser working together."""

    def test_search_code_then_parse_logs(self, tmp_path: Path) -> None:
        """Should find error handler in code, then parse related logs."""
        # Create source code with error handler
        app_code = tmp_path / "app.py"
        app_code.write_text(
            "import logging\n\n"
            "logger = logging.getLogger(__name__)\n\n"
            "def handle_request(data):\n"
            "    try:\n"
            "        return process(data)\n"
            "    except ValueError as e:\n"
            '        logger.error(f"Request failed: {e}")\n'
            "        raise\n",
            encoding="utf-8",
        )

        # Create a log file with matching errors
        log_file = tmp_path / "app.log"
        log_file.write_text(
            "2024-01-15 10:00:00 ERROR [app] Request failed: invalid input\n"
            "Traceback (most recent call last):\n"
            '  File "app.py", line 8, in handle_request\n'
            "    return process(data)\n"
            "ValueError: invalid input\n",
            encoding="utf-8",
        )

        # Step 1: Search code for error handling
        code_results = code_search.invoke({
            "pattern": "ValueError",
            "path": str(tmp_path),
            "extensions": ".py",
        })
        assert len(code_results) >= 1

        # Step 2: Parse the log file
        log_content = log_file.read_text(encoding="utf-8")
        log_entries = log_parser.invoke({"content": log_content})
        assert isinstance(log_entries, list)
        assert len(log_entries) >= 1

        error_entries = [e for e in log_entries if e.get("level") == "ERROR"]
        assert len(error_entries) >= 1

    def test_search_and_parse_with_multiple_files(self, tmp_path: Path) -> None:
        """Should search across multiple source files and parse combined logs."""
        # Create multiple source files
        (tmp_path / "auth.py").write_text(
            "def authenticate(token):\n"
            "    if not token:\n"
            '        raise AuthError("Missing token")\n',
            encoding="utf-8",
        )
        (tmp_path / "api.py").write_text(
            "def call_api(url):\n"
            "    response = requests.get(url)\n"
            "    if response.status_code != 200:\n"
            '        raise APIError(f"HTTP {response.status_code}")\n',
            encoding="utf-8",
        )

        # Create a log with entries from both modules
        (tmp_path / "app.log").write_text(
            "2024-01-15 10:00:00 ERROR [auth] AuthError: Missing token\n"
            "2024-01-15 10:00:01 ERROR [api] APIError: HTTP 500\n",
            encoding="utf-8",
        )

        # Search for error patterns across codebase
        results = code_search.invoke({
            "pattern": "raise",
            "path": str(tmp_path),
            "extensions": ".py",
        })
        assert len(results) >= 2  # Should find both auth.py and api.py

        # Parse the combined log
        log_content = (tmp_path / "app.log").read_text(encoding="utf-8")
        entries = log_parser.invoke({"content": log_content})
        error_entries = [e for e in entries if e.get("level") == "ERROR"]
        assert len(error_entries) == 2


@pytest.mark.integration
class TestDiagnosticWorkflow:
    """Test a simulated diagnostic workflow."""

    def test_full_diagnostic_flow(self, tmp_path: Path) -> None:
        """Should simulate a complete diagnostic flow with available tools."""
        # Setup: application code with a bug
        (tmp_path / "processor.py").write_text(
            "def process_batch(items):\n"
            "    results = []\n"
            "    for item in items:\n"
            "        results.append(transform(item))\n"
            "    return results\n\n"
            "def transform(item):\n"
            "    if item is None:\n"
            '        raise TypeError("Cannot transform None")\n'
            "    return item.upper()\n",
            encoding="utf-8",
        )

        # Setup: log showing the error
        (tmp_path / "worker.log").write_text(
            "2024-01-15 14:00:00 ERROR [worker] Batch processing failed\n"
            "Traceback (most recent call last):\n"
            '  File "processor.py", line 4, in process_batch\n'
            "    results.append(transform(item))\n"
            '  File "processor.py", line 10, in transform\n'
            '    raise TypeError("Cannot transform None")\n'
            "TypeError: Cannot transform None\n",
            encoding="utf-8",
        )

        # Step 1: Find the error source in code
        code_hits = code_search.invoke({
            "pattern": "Cannot transform None",
            "path": str(tmp_path),
            "extensions": ".py",
        })
        assert len(code_hits) >= 1
        assert "processor.py" in code_hits[0].get("file", "")

        # Step 2: Parse the error log
        log_content = (tmp_path / "worker.log").read_text(encoding="utf-8")
        entries = log_parser.invoke({"content": log_content})
        errors = [e for e in entries if e.get("level") == "ERROR"]
        assert len(errors) >= 1
        assert "Batch processing failed" in errors[0]["message"]

        # Step 3: Search for related code patterns
        batch_hits = code_search.invoke({
            "pattern": "process_batch",
            "path": str(tmp_path),
            "extensions": ".py",
        })
        assert len(batch_hits) >= 1
