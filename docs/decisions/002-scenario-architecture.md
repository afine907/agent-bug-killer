# ADR-002: Scenario-Based Architecture

## Status

Accepted

## Context

The project needs to support multiple diagnostic scenarios (log analysis, bug diagnosis, etc.) while sharing common infrastructure. We need to decide how to organize code for maximum reuse and independence.

## Decision

Adopt a scenario-based architecture with shared core:

```
core/           # Shared infrastructure (agents, tools, config)
scenarios/      # Independent scenario implementations
  log_analyzer/ # Scenario 1: reads and parses log files
  bug_diagnoser/# Scenario 2: multi-source bug diagnosis
  scenario-3/   # Placeholder for future scenarios
```

Each scenario is self-contained with its own:
- Agent definition and system prompt
- Tools (can reuse core tools)
- CLI entry point
- Tests

### Key Principles
1. **Scenario Independence**: Each scenario can run and test independently
2. **Tool Reuse**: Common tools (log_parser) live in scenarios but can be imported
3. **Core Abstraction**: base_agent.py and base_tool.py provide factory patterns
4. **Prompt Externalization**: System prompts stored as markdown files, loaded at runtime

## Consequences

### Positive
- Easy to add new scenarios without touching existing code
- Clear separation of concerns
- Each scenario can evolve independently
- Tests are scoped and fast

### Negative
- Some code duplication across scenarios (e.g., CLI setup)
- Need to maintain import paths carefully
- Cross-scenario tool imports create coupling

### Mitigations
- Extract common CLI patterns to core/ if duplication becomes problematic
- Use absolute imports consistently
- Document cross-scenario dependencies
