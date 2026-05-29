"""Tests for Agent Bug Killer API."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_returns_ok(self, client: TestClient) -> None:
        """Should return ok status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


class TestAnalyzeLogEndpoint:
    """Tests for log analysis endpoint."""

    def test_analyze_log_text(self, client: TestClient) -> None:
        """Should analyze log text."""
        response = client.post(
            "/api/v1/analyze-log",
            json={"log_text": "2024-01-15 10:00:00 ERROR [app] Test error\n"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_errors" in data
        assert "errors" in data

    def test_analyze_log_missing_input(self, client: TestClient) -> None:
        """Should return 400 when no input provided."""
        response = client.post("/api/v1/analyze-log", json={})
        assert response.status_code == 400

    def test_analyze_log_nonexistent_file(self, client: TestClient) -> None:
        """Should return 400 for nonexistent file."""
        response = client.post(
            "/api/v1/analyze-log",
            json={"file_path": "/nonexistent/file.log"},
        )
        assert response.status_code == 400


class TestDiagnoseEndpoint:
    """Tests for diagnosis endpoint."""

    def test_diagnose_returns_response(self, client: TestClient) -> None:
        """Should return diagnosis response."""
        response = client.post(
            "/api/v1/diagnose",
            json={"bug_description": "App crashes on startup"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "recommendations" in data

    def test_diagnose_missing_description(self, client: TestClient) -> None:
        """Should return 422 when description missing."""
        response = client.post("/api/v1/diagnose", json={})
        assert response.status_code == 422


class TestHistoryEndpoints:
    """Tests for history endpoints."""

    def test_list_history(self, client: TestClient) -> None:
        """Should list history entries."""
        response = client.get("/api/v1/history")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "entries" in data

    def test_get_nonexistent_report(self, client: TestClient) -> None:
        """Should return 404 for nonexistent report."""
        response = client.get("/api/v1/history/nonexistent")
        assert response.status_code == 404

    def test_delete_nonexistent_report(self, client: TestClient) -> None:
        """Should return 404 for nonexistent report."""
        response = client.delete("/api/v1/history/nonexistent")
        assert response.status_code == 404

    def test_search_history(self, client: TestClient) -> None:
        """Should search history."""
        response = client.get("/api/v1/history/search/test")
        assert response.status_code == 200
