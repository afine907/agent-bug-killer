"""Tests for core.planner module."""

from __future__ import annotations

from core.planner import (
    create_diagnostic_plan,
    create_log_analysis_plan,
    format_plan_summary,
)


class TestCreateDiagnosticPlan:
    """Tests for create_diagnostic_plan function."""

    def test_returns_five_steps(self) -> None:
        """Test that diagnostic plan has 5 steps."""
        plan = create_diagnostic_plan("App crashes on startup")
        assert len(plan) == 5

    def test_first_step_in_progress(self) -> None:
        """Test that first step is marked in_progress."""
        plan = create_diagnostic_plan("test bug")
        assert plan[0]["status"] == "in_progress"

    def test_remaining_steps_pending(self) -> None:
        """Test that remaining steps are pending."""
        plan = create_diagnostic_plan("test bug")
        for item in plan[1:]:
            assert item["status"] == "pending"

    def test_includes_bug_description(self) -> None:
        """Test that bug description appears in first step."""
        desc = "Database connection timeout"
        plan = create_diagnostic_plan(desc)
        assert desc in plan[0]["content"]


class TestCreateLogAnalysisPlan:
    """Tests for create_log_analysis_plan function."""

    def test_returns_five_steps(self) -> None:
        """Test that log analysis plan has 5 steps."""
        plan = create_log_analysis_plan("/var/log/app.log")
        assert len(plan) == 5

    def test_includes_log_path(self) -> None:
        """Test that log path appears in first step."""
        plan = create_log_analysis_plan("/var/log/app.log")
        assert "/var/log/app.log" in plan[0]["content"]


class TestFormatPlanSummary:
    """Tests for format_plan_summary function."""

    def test_format_empty_plan(self) -> None:
        """Test formatting an empty plan."""
        assert format_plan_summary([]) == ""

    def test_format_with_statuses(self) -> None:
        """Test formatting shows correct icons."""
        todos = [
            {"content": "Step 1", "status": "completed"},
            {"content": "Step 2", "status": "in_progress"},
            {"content": "Step 3", "status": "pending"},
        ]
        result = format_plan_summary(todos)
        assert "✅ Step 1" in result
        assert "🔄 Step 2" in result
        assert "⏳ Step 3" in result

    def test_format_unknown_status(self) -> None:
        """Test formatting with unknown status."""
        todos = [{"content": "Unknown", "status": "custom"}]
        result = format_plan_summary(todos)
        assert "❓ Unknown" in result
