"""Shared test fixtures for log-analyzer scenario."""

from pathlib import Path

import pytest

SAMPLE_LOGS_DIR = Path(__file__).parent / "sample_logs"


@pytest.fixture
def sample_logs_dir() -> Path:
    """Return the path to sample logs directory."""
    return SAMPLE_LOGS_DIR


@pytest.fixture
def python_exception_log() -> str:
    """Return a sample Python exception log."""
    return """2024-01-15 10:30:15,123 ERROR [web.app] Request failed
Traceback (most recent call last):
  File "/app/web/views.py", line 42, in handle_request
    result = process_data(request.data)
  File "/app/core/processor.py", line 87, in process_data
    return json.loads(raw_data)
  File "/usr/lib/python3.12/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

2024-01-15 10:30:15,456 INFO [web.app] Request processed in 0.33s
"""


@pytest.fixture
def multiline_stack_log() -> str:
    """Return a sample multiline stack trace log."""
    return """2024-01-15 11:00:00,001 ERROR [db.connection] Database connection failed
Traceback (most recent call last):
  File "/app/db/pool.py", line 15, in get_connection
    conn = psycopg2.connect(self.dsn)
  File "/app/db/pool.py", line 28, in connect
    raise ConnectionError(f"Cannot connect to {host}:{port}")
ConnectionError: Cannot connect to db-primary:5432

2024-01-15 11:00:00,100 WARNING [db.pool] Retrying connection (attempt 1/3)
2024-01-15 11:00:05,200 ERROR [db.pool] All retry attempts exhausted
"""


@pytest.fixture
def mixed_levels_log() -> str:
    """Return a log with mixed severity levels."""
    return """2024-01-15 12:00:00,001 INFO [startup] Application starting
2024-01-15 12:00:01,002 DEBUG [config] Loading configuration from /etc/app.conf
2024-01-15 12:00:01,500 INFO [startup] Configuration loaded successfully
2024-01-15 12:00:02,003 WARNING [scheduler] Task queue depth is 45/50
2024-01-15 12:00:03,004 ERROR [scheduler] Task execution failed: timeout after 30s
2024-01-15 12:00:03,500 INFO [scheduler] Task marked as failed, continuing
2024-01-15 12:00:04,005 DEBUG [metrics] CPU usage: 87%
2024-01-15 12:00:05,006 ERROR [worker] Worker process killed: OOM
"""


@pytest.fixture
def empty_log() -> str:
    """Return an empty log string."""
    return ""


@pytest.fixture
def mixed_exception_log() -> str:
    """Return a log with multiple different exception types."""
    return """2024-01-15 13:00:00,001 ERROR [api.client] API call failed
requests.exceptions.Timeout: HTTPSConnectionPool(host='api.example.com', port=443): Read timed out.
(read timeout=5)

2024-01-15 13:00:01,002 ERROR [auth.service] Authentication failed
ValueError: Invalid token format: expected 3 parts, got 2

2024-01-15 13:00:02,003 ERROR [cache.redis] Cache write failed
redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379. Connection refused.
"""
