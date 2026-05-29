#!/usr/bin/env bash
# Agent Bug Killer — Test Runner Script
# Usage:
#   ./scripts/run_tests.sh              # Run all tests
#   ./scripts/run_tests.sh log-analyzer # Run log-analyzer tests only
#   ./scripts/run_tests.sh bug-diagnoser # Run bug-diagnoser tests only
#   ./scripts/run_tests.sh core         # Run core framework tests only
#   ./scripts/run_tests.sh --coverage   # Run all tests with coverage report
#   ./scripts/run_tests.sh --lint       # Run ruff lint check

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

run_lint() {
    echo "=== Running ruff lint ==="
    uv run ruff check .
    echo "=== Lint passed ==="
}

run_tests() {
    local extra_args=("$@")
    echo "=== Running tests ==="
    uv run pytest --tb=short -q "${extra_args[@]}"
    echo "=== Tests passed ==="
}

run_coverage() {
    echo "=== Running tests with coverage ==="
    uv run pytest --tb=short -q --cov=core --cov=scenarios --cov-report=term-missing --cov-report=html:htmlcov
    echo "=== Coverage report generated at htmlcov/index.html ==="
}

case "${1:-all}" in
    all)
        run_tests
        ;;
    log-analyzer)
        run_tests "scenarios/log_analyzer/tests/"
        ;;
    bug-diagnoser)
        run_tests "scenarios/bug_diagnoser/tests/"
        ;;
    core)
        run_tests "core/tests/"
        ;;
    --coverage)
        run_coverage
        ;;
    --lint)
        run_lint
        ;;
    --full)
        run_lint
        run_coverage
        ;;
    *)
        echo "Usage: $0 [all|log-analyzer|bug-diagnoser|core|--coverage|--lint|--full]"
        exit 1
        ;;
esac
