# Learnings: Agent Development

Key lessons learned during the development of Agent Bug Killer.

## Tool Design

### 1. Tools Should Return Structured Data
- LangChain tools can return strings or dicts
- For agent consumption, structured dicts work better
- For human display, formatted strings are preferred
- **Solution**: Return structured data, let the CLI format for display

### 2. Tool Error Handling Matters
- Agents can get confused by cryptic error messages
- Always return actionable error information
- Include what went wrong AND what to try next
- Example: "File not found: /path/to/file. Check if the path is correct."

### 3. Tool Descriptions Are Prompts
- The tool's docstring becomes part of the agent's context
- Be specific about input/output formats
- Include examples in docstrings when helpful

## Prompt Engineering

### 1. System Prompts Should Be External
- Hardcoded prompts in Python are hard to iterate on
- Markdown files allow non-developers to review and edit
- Version control tracks prompt evolution separately from code

### 2. Structured Output Requires Explicit Instructions
- LLMs don't always return valid JSON
- Specify the exact JSON schema in the prompt
- Consider using response_format parameter when available

### 3. Few-Shot Examples Help Consistency
- Include example input/output pairs in system prompt
- Shows the agent exactly what format you expect
- Reduces variance in output quality

## Testing

### 1. Mock at the Right Level
- Mock LLM calls for unit tests (fast, deterministic)
- Use real tools with temp files for integration tests
- Reserve real LLM calls for manual E2E testing

### 2. Test Tool Interoperability
- Tools often chain together (read → parse → analyze)
- Integration tests catch issues unit tests miss
- Use pytest fixtures for shared test data

### 3. Snapshot Testing for Prompts
- Prompt changes can subtly break agent behavior
- Consider snapshot tests for system prompts
- Review prompt diffs carefully in PRs

## Architecture

### 1. Thin Wrappers Over Frameworks
- core/base_agent.py wraps DeepAgents with 40 lines
- Provides stable API even if framework changes
- Easy to swap frameworks if needed

### 2. Configuration via Environment
- pydantic-settings for type-safe config
- .env files for local development
- Environment variables for CI/production
- Never hardcode API keys or timeouts

### 3. Incremental Complexity
- Phase 1: Single tool, simple flow
- Phase 2: Multi-tool, parallel execution
- Phase 3: Multi-agent, memory, planning
- Each phase builds on the previous
