# Contributing to Agent Bug Killer

Thank you for your interest in contributing!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/agent-bug-killer.git
   cd agent-bug-killer
   ```

2. **Install uv** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Development Workflow

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run checks**
   ```bash
   # Lint
   uv run ruff check .

   # Format
   uv run ruff format .

   # Type check
   uv run mypy core/ scenarios/

   # Tests
   uv run pytest
   ```

4. **Commit your changes**
   ```bash
   git add -A
   git commit -m "feat(scope): description"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- **Python 3.12+** with type annotations
- **Line length**: 100 characters
- **Imports**: Sorted with ruff (isort-compatible)
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Docstrings**: Google style for all public functions and classes

## Commit Messages

Follow Conventional Commits:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `ci`, `perf`, `style`, `chore`

Scopes: `core`, `log-analyzer`, `bug-diagnoser`, `api`, `docs`, `ci`

## Testing

- **Unit tests**: Fast, no external dependencies, mock LLM calls
- **Integration tests**: Real tool calls with temp files/directories
- **E2E tests**: Full flow with real LLM (manual, not in CI)

Run specific test types:
```bash
uv run pytest -m unit        # Unit tests only
uv run pytest -m integration # Integration tests only
```

## Project Structure

```
core/                    # Shared infrastructure
scenarios/               # Independent scenario implementations
  log_analyzer/          # Scenario 1: Log analysis
  bug_diagnoser/         # Scenario 2: Bug diagnosis
docs/                    # Documentation
scripts/                 # Utility scripts
```

## Questions?

Open an issue or reach out to the maintainers.
