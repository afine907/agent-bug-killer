"""Metrics collection for monitoring.

Collects and exposes metrics for Prometheus integration.
"""

from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class MetricPoint:
    """A single metric data point."""

    name: str
    value: float
    labels: dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class MetricsCollector:
    """Collects and manages metrics."""

    def __init__(self) -> None:
        """Initialize metrics collector."""
        self._counters: dict[str, float] = defaultdict(float)
        self._gauges: dict[str, float] = {}
        self._histograms: dict[str, list[float]] = defaultdict(list)
        self._labels: dict[str, dict[str, str]] = {}

    def increment(
        self,
        name: str,
        value: float = 1.0,
        labels: dict[str, str] | None = None,
    ) -> None:
        """Increment a counter metric.

        Args:
            name: Metric name.
            value: Value to increment by.
            labels: Optional labels for the metric.
        """
        key = self._make_key(name, labels)
        self._counters[key] += value
        if labels:
            self._labels[key] = labels

    def set_gauge(
        self,
        name: str,
        value: float,
        labels: dict[str, str] | None = None,
    ) -> None:
        """Set a gauge metric.

        Args:
            name: Metric name.
            value: Gauge value.
            labels: Optional labels for the metric.
        """
        key = self._make_key(name, labels)
        self._gauges[key] = value
        if labels:
            self._labels[key] = labels

    def observe(
        self,
        name: str,
        value: float,
        labels: dict[str, str] | None = None,
    ) -> None:
        """Observe a value for histogram metric.

        Args:
            name: Metric name.
            value: Observed value.
            labels: Optional labels for the metric.
        """
        key = self._make_key(name, labels)
        self._histograms[key].append(value)
        if labels:
            self._labels[key] = labels

    def get_counter(
        self,
        name: str,
        labels: dict[str, str] | None = None,
    ) -> float:
        """Get counter value.

        Args:
            name: Metric name.
            labels: Optional labels.

        Returns:
            Counter value.
        """
        key = self._make_key(name, labels)
        return self._counters.get(key, 0.0)

    def get_gauge(
        self,
        name: str,
        labels: dict[str, str] | None = None,
    ) -> float | None:
        """Get gauge value.

        Args:
            name: Metric name.
            labels: Optional labels.

        Returns:
            Gauge value or None.
        """
        key = self._make_key(name, labels)
        return self._gauges.get(key)

    def get_histogram(
        self,
        name: str,
        labels: dict[str, str] | None = None,
    ) -> list[float]:
        """Get histogram values.

        Args:
            name: Metric name.
            labels: Optional labels.

        Returns:
            List of observed values.
        """
        key = self._make_key(name, labels)
        return self._histograms.get(key, [])

    def get_all_metrics(self) -> list[MetricPoint]:
        """Get all metrics as data points.

        Returns:
            List of MetricPoint objects.
        """
        points = []

        # Counters
        for key, value in self._counters.items():
            name = key.split("{")[0]
            labels = self._labels.get(key, {})
            points.append(MetricPoint(name=name, value=value, labels=labels))

        # Gauges
        for key, value in self._gauges.items():
            name = key.split("{")[0]
            labels = self._labels.get(key, {})
            points.append(MetricPoint(name=name, value=value, labels=labels))

        # Histograms (summarize)
        for key, values in self._histograms.items():
            name = key.split("{")[0]
            labels = self._labels.get(key, {})
            if values:
                points.append(MetricPoint(
                    name=f"{name}_count",
                    value=len(values),
                    labels=labels,
                ))
                points.append(MetricPoint(
                    name=f"{name}_sum",
                    value=sum(values),
                    labels=labels,
                ))

        return points

    def reset(self) -> None:
        """Reset all metrics."""
        self._counters.clear()
        self._gauges.clear()
        self._histograms.clear()
        self._labels.clear()

    def _make_key(
        self,
        name: str,
        labels: dict[str, str] | None = None,
    ) -> str:
        """Create metric key with labels."""
        if not labels:
            return name
        label_str = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"


# Global metrics collector
metrics = MetricsCollector()


# Common metric names
class MetricNames:
    """Standard metric names."""

    # Request metrics
    REQUEST_COUNT = "abk_requests_total"
    REQUEST_DURATION = "abk_request_duration_seconds"

    # Analysis metrics
    ANALYSIS_COUNT = "abk_analyses_total"
    ANALYSIS_DURATION = "abk_analysis_duration_seconds"
    ANALYSIS_ERRORS = "abk_analysis_errors_total"

    # Diagnosis metrics
    DIAGNOSIS_COUNT = "abk_diagnoses_total"
    DIAGNOSIS_DURATION = "abk_diagnosis_duration_seconds"

    # Tool metrics
    TOOL_CALLS = "abk_tool_calls_total"
    TOOL_DURATION = "abk_tool_duration_seconds"
    TOOL_ERRORS = "abk_tool_errors_total"

    # Knowledge base metrics
    KB_QUERIES = "abk_kb_queries_total"
    KB_HITS = "abk_kb_hits_total"

    # System metrics
    ACTIVE_SESSIONS = "abk_active_sessions"
    CACHE_HITS = "abk_cache_hits_total"
    CACHE_MISSES = "abk_cache_misses_total"
