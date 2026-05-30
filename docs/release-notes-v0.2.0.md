# Release Notes — Version 0.2.0

**Release Date**: January 20, 2024

## Overview

Version 0.2.0 is a major quality release that brings Agent Bug Killer
to production readiness through 200 rounds of iterative improvement.

## What's New

### Web API
- RESTful API with FastAPI
- 12 endpoints for log analysis, diagnosis, history, and knowledge base
- Request logging and rate limiting middleware
- Pydantic validation for all inputs

### Docker Support
- Production-ready Dockerfile
- docker-compose.yml for easy deployment
- Non-root container user
- Health check configuration

### Quality Improvements
- Type-safe code (0 mypy errors)
- 241 tests with 91% coverage
- Comprehensive error handling
- Input validation for all tools
- Retry logic with exponential backoff
- Progress tracking utilities
- Caching utilities

### Documentation
- Complete API reference
- Contributing guide
- Security policy
- Architecture decision records
- Quality reports

## Breaking Changes

None. This release is fully backward compatible with v0.1.0.

## Upgrade Guide

```bash
# Update to latest version
git pull origin main

# Install new dependencies
uv sync

# Run tests to verify
uv run pytest
```

## Known Issues

- CDP tools require websockets library (optional dependency)
- SSH tools require paramiko library
- Some edge cases in CDP tool coverage (46%)

## Contributors

- AI Agent (Claude) - Primary developer
- Human oversight - Architecture and review

## Next Release

v0.3.0 will focus on:
- PostgreSQL database backend
- API key authentication
- Prometheus monitoring
- Performance optimization

## Changelog

See [CHANGELOG.md](../CHANGELOG.md) for detailed changes.

## Downloads

- Source: [GitHub](https://github.com/afine907/agent-bug-killer)
- Docker: `docker pull agent-bug-killer:0.2.0`

## Support

- Issues: [GitHub Issues](https://github.com/afine907/agent-bug-killer/issues)
- Docs: [Documentation](./)
- Security: [SECURITY.md](../SECURITY.md)
