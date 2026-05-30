# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2024-02-15

### Added
- Error grouping and aggregation (Sentry-inspired fingerprinting)
- Advanced RCA engine with multi-technique analysis and confidence scoring
- Metrics collection system (Counter, Gauge, Histogram)
- Dynamic prompt loading from markdown files with fallback
- Memory system wrapper over DeepAgents MemoryMiddleware
- Planning helpers for diagnostic workflows
- Comprehensive documentation (getting started, best practices, FAQ, architecture)
- Community guidelines and contributing guide
- Competitor analysis documentation

### Changed
- Agents now load prompts from markdown files instead of hardcoded strings
- Improved project metadata (keywords, classifiers, project URLs)

## [0.2.0] - 2024-01-20

### Added
- FastAPI web API with health, log analysis, diagnosis, and history endpoints
- Multi-format report output (JSON, Markdown, HTML)
- Diagnostic history storage with search
- Root cause analysis module with 7 error patterns
- Knowledge base for error patterns and solutions
- Fix suggestions generation
- Docker containerization
- API middleware (logging, rate limiting)
- GitHub Actions CI/CD
- Comprehensive documentation (ADRs, learnings, contributing guide)
- Retry logic with exponential backoff
- Input validation utilities
- Progress tracking utilities
- Custom exception hierarchy
- Caching utilities
- CLI tests (100% coverage)
- Type-safe code (0 mypy errors)

### Changed
- Improved settings with validation and documentation
- Enhanced CLI with --format option
- Fixed README project structure
- Improved SSH tool error handling
- Improved CDP tool error handling
- Version bump to 0.2.0

## [0.1.0] - 2024-01-15

### Added
- Initial release
- Log Analyzer Agent (Phase 1)
- Bug Diagnoser Agent (Phase 2)
- Core framework (base_agent, base_tool, settings)
- Unit and integration tests
