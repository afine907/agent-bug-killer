"""Tests for core.metrics module."""

from __future__ import annotations

import pytest

from core.metrics import MetricNames, MetricsCollector


@pytest.fixture
def collector() -> MetricsCollector:
    """Create a MetricsCollector instance."""
    return MetricsCollector()


class TestMetricsCollector:
    """Tests for MetricsCollector class."""

    def test_increment_counter(self, collector: MetricsCollector) -> None:
        """Should increment counter."""
        collector.increment("test_counter")
        assert collector.get_counter("test_counter") == 1.0

    def test_increment_counter_with_value(self, collector: MetricsCollector) -> None:
        """Should increment counter by value."""
        collector.increment("test_counter", 5.0)
        assert collector.get_counter("test_counter") == 5.0

    def test_increment_counter_multiple(self, collector: MetricsCollector) -> None:
        """Should accumulate counter values."""
        collector.increment("test_counter")
        collector.increment("test_counter")
        collector.increment("test_counter")
        assert collector.get_counter("test_counter") == 3.0

    def test_set_gauge(self, collector: MetricsCollector) -> None:
        """Should set gauge value."""
        collector.set_gauge("test_gauge", 42.0)
        assert collector.get_gauge("test_gauge") == 42.0

    def test_gauge_overwrite(self, collector: MetricsCollector) -> None:
        """Should overwrite gauge value."""
        collector.set_gauge("test_gauge", 1.0)
        collector.set_gauge("test_gauge", 2.0)
        assert collector.get_gauge("test_gauge") == 2.0

    def test_observe_histogram(self, collector: MetricsCollector) -> None:
        """Should observe histogram values."""
        collector.observe("test_histogram", 1.0)
        collector.observe("test_histogram", 2.0)
        collector.observe("test_histogram", 3.0)
        values = collector.get_histogram("test_histogram")
        assert len(values) == 3
        assert values == [1.0, 2.0, 3.0]

    def test_counter_with_labels(self, collector: MetricsCollector) -> None:
        """Should handle labels."""
        collector.increment("requests", labels={"method": "GET"})
        collector.increment("requests", labels={"method": "POST"})
        assert collector.get_counter("requests", labels={"method": "GET"}) == 1.0
        assert collector.get_counter("requests", labels={"method": "POST"}) == 1.0

    def test_get_all_metrics(self, collector: MetricsCollector) -> None:
        """Should return all metrics."""
        collector.increment("counter1")
        collector.set_gauge("gauge1", 42.0)
        collector.observe("hist1", 1.0)

        metrics = collector.get_all_metrics()
        assert len(metrics) >= 3

    def test_reset(self, collector: MetricsCollector) -> None:
        """Should reset all metrics."""
        collector.increment("counter1")
        collector.set_gauge("gauge1", 42.0)
        collector.reset()

        assert collector.get_counter("counter1") == 0.0
        assert collector.get_gauge("gauge1") is None

    def test_nonexistent_counter(self, collector: MetricsCollector) -> None:
        """Should return 0 for nonexistent counter."""
        assert collector.get_counter("nonexistent") == 0.0

    def test_nonexistent_gauge(self, collector: MetricsCollector) -> None:
        """Should return None for nonexistent gauge."""
        assert collector.get_gauge("nonexistent") is None

    def test_nonexistent_histogram(self, collector: MetricsCollector) -> None:
        """Should return empty list for nonexistent histogram."""
        assert collector.get_histogram("nonexistent") == []


class TestMetricNames:
    """Tests for MetricNames constants."""

    def test_has_request_metrics(self) -> None:
        """Should have request metric names."""
        assert hasattr(MetricNames, "REQUEST_COUNT")
        assert hasattr(MetricNames, "REQUEST_DURATION")

    def test_has_analysis_metrics(self) -> None:
        """Should have analysis metric names."""
        assert hasattr(MetricNames, "ANALYSIS_COUNT")
        assert hasattr(MetricNames, "ANALYSIS_DURATION")
