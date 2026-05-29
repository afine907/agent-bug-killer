# ADR-001: Technology Stack Selection

## Status

Accepted

## Context

We need to select a technology stack for building an AI Agent that diagnoses production bugs. The stack must support:
- LLM integration with tool use capabilities
- Multi-tool orchestration (SSH, CDP, file system)
- Async operations for I/O-bound tasks
- Testing with mocked LLM calls
- CLI and potential future web interface

## Decision

### Agent Framework: LangChain DeepAgents
- **Why**: Official LangChain framework with built-in planning, memory, and sub-agent support. Wraps LangGraph for state management.
- **Alternatives considered**: Raw LangGraph (more control but more boilerplate), AutoGen (multi-agent focused but less tool support), CrewAI (higher abstraction but less flexibility)

### LLM: Claude via langchain-anthropic
- **Why**: Excellent tool use support, strong Chinese language capabilities, competitive pricing.
- **Alternatives considered**: GPT-4 (good tool use but more expensive), Gemini (weaker tool use at time of decision)

### Package Manager: uv
- **Why**: Fast, modern, recommended by DeepAgents documentation. Better dependency resolution than pip.
- **Alternatives considered**: pip (standard but slow), poetry (good but heavier), pdm (similar to uv but less adoption)

### Testing: pytest + pytest-asyncio
- **Why**: Standard Python testing framework with excellent async support and fixture system.
- **Alternatives considered**: unittest (verbose), nose2 (declining maintenance)

## Consequences

### Positive
- DeepAgents provides planning and memory out of the box
- Claude's tool use reduces prompt engineering effort
- uv provides fast dependency resolution
- pytest fixtures simplify test setup

### Negative
- DeepAgents is relatively new, may have breaking changes
- Claude API may have rate limits during heavy testing
- uv requires separate installation from pip

### Risks
- DeepAgents API changes could require significant refactoring
- Mitigation: Pin versions, abstract behind core/ layer
