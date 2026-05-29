# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

### Changed
- Improved settings with validation and documentation
- Enhanced CLI with --format option
- Fixed README project structure

## [0.1.0] - 2024-01-15

### Added
- Initial release
- Log Analyzer Agent (Phase 1)
- Bug Diagnoser Agent (Phase 2)
- Core framework (base_agent, base_tool, settings)
- Unit and integration tests
