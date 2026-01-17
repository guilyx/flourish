# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of bash.ai
- `ask` command for direct LLM interaction without command execution
- `agent` command with code execution capabilities using Google ADK
- Allowlist and blacklist support for command execution security
- Support for multiple Gemini models via configuration
- Rich CLI output with markdown formatting
- Comprehensive documentation (README, CONTRIBUTING, LICENSE, SECURITY)
- GitHub Actions CI/CD pipeline
- Pre-commit hooks configuration
- Python project structure with uv

### Security
- Command allowlist/blacklist enforcement
- API key management via environment variables
- Security-focused agent instructions

## [0.1.0] - 2025-01-16

### Added
- Initial release
