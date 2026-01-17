# Contributing to bash.ai

Thank you for your interest in contributing to bash.ai! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/made-after-dark/bash.ai/issues)
2. If not, create a new issue with:
   - A clear, descriptive title
   - Steps to reproduce the bug
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)
   - Relevant logs or error messages

### Suggesting Features

1. Check existing [Issues](https://github.com/made-after-dark/bash.ai/issues) and [Discussions](https://github.com/made-after-dark/bash.ai/discussions)
2. Create a new issue or discussion thread with:
   - A clear description of the feature
   - Use cases and examples
   - Potential implementation approach (if you have ideas)

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/bash.ai.git
   cd bash.ai
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Set up development environment**
   ```bash
   # Install uv if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install dependencies
   uv sync --dev

   # Install pre-commit hooks
   uv run pre-commit install
   ```

4. **Make your changes**
   - Write clean, maintainable code
   - Follow Python best practices (PEP 8)
   - Add tests for new functionality
   - Update documentation as needed

5. **Run checks locally**
   ```bash
   uv run ruff check .
   uv run black --check .
   uv run mypy bash_ai
   uv run pytest
   ```

6. **Commit your changes**
   ```bash
   git commit -m "Short commit message (max 70 chars)" \
              -m "Extended description of what and why"
   ```

   Follow the commit message guidelines:
   - First line: 70 characters max, imperative mood
   - Second line: Extended description (unlimited)
   - Reference issues: `Fixes #123` or `Closes #456`

7. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

   Then create a PR on GitHub with:
   - Clear title and description
   - Reference to related issues
   - Screenshots/examples if applicable

## Development Guidelines

### Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use `black` for formatting (line length: 100)
- Use `ruff` for linting
- Maximum line length: 100 characters
- Use type hints where appropriate

### Testing

- Write tests for all new features
- Maintain or improve test coverage
- Use `pytest` for testing
- Test error cases and edge conditions

### Documentation

- Update README.md for user-facing changes
- Add docstrings for all functions and classes
- Update CONTRIBUTING.md if process changes
- Keep commit messages clear and descriptive

### Dependencies

- Minimize external dependencies
- Use standard library when possible
- Keep dependencies up to date
- Document why new dependencies are needed

## Project Structure

```
bash.ai/
├── bash_ai/              # Main package
│   ├── __init__.py
│   ├── config.py         # Configuration
│   ├── agents.py         # Agent definitions
│   ├── runner.py         # Agent execution
│   └── cli.py            # CLI interface
├── tests/                # Test files
└── ...
```

## Review Process

1. All PRs require at least one approval
2. CI must pass (lint, test, build)
3. Code review feedback will be addressed
4. Maintainers will merge when ready

## Questions?

- Open a [Discussion](https://github.com/made-after-dark/bash.ai/discussions)
- Check existing [Issues](https://github.com/made-after-dark/bash.ai/issues)
- Reach out to maintainers

Thank you for contributing to bash.ai! 🚀
