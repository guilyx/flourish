# bash.ai

> AI-powered bash environment enhancement tool using Google ADK

`bash.ai` is an open-source tool that enhances your bash environment with agentic AI capabilities. It allows you to interact with LLMs directly from your terminal and execute complex workflows through AI orchestration.

## Features

- **Ask Mode**: Direct LLM interaction without command execution
  ```bash
  bash-ai ask "What is the difference between git merge and rebase?"
  ```

- **Agent Mode**: AI agent with command execution capabilities
  ```bash
  bash-ai agent "List all files in the current directory and show git status"
  ```

- **Security Controls**: Allowlist and blacklist for command execution
  ```bash
  bash-ai agent --allowlist "ls,cd,git" "Check git status"
  bash-ai agent --blacklist "rm,dd" "Help me organize files"
  ```

- **AI-Enhanced Bash**: Auto-completion suggestions and intelligent command assistance

## Prerequisites

- Python 3.12 or later
- Google ADK API key ([Get one here](https://aistudio.google.com/apikey))

### Upgrading Python

If you need to upgrade Python, you can use:

```bash
# Using pyenv (recommended)
pyenv install 3.12.0
pyenv global 3.12.0

# Or download from python.org
```

## Installation

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/made-after-dark/bash.ai.git
   cd bash.ai
   ```

2. Install [uv](https://github.com/astral-sh/uv) (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Set up your API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

   The `.env` file is automatically loaded - no need to `source` it!

5. Install the CLI tool:
   ```bash
   uv pip install -e .
   ```

6. **Activate the virtual environment** (or use `uv run`):
   ```bash
   # Option 1: Activate venv
   source .venv/bin/activate

   # Option 2: Use uv run (recommended)
   uv run bash-ai ask "Hello"
   ```

   To make `bash-ai` available globally, add to your `~/.bashrc` or `~/.zshrc`:
   ```bash
   export PATH="$PATH:/path/to/bash.ai/.venv/bin"
   ```

## Usage

### Basic Usage

**Ask a question (no command execution):**
```bash
bash-ai ask "Explain how Docker containers work"
```

**Use agent with command execution:**
```bash
bash-ai agent "Find all .py files in the current directory"
```

### Advanced Usage

**With allowlist (only allow specific commands):**
```bash
bash-ai agent --allowlist "ls,cd,git,find" "Show me git status and list files"
```

**With blacklist (prevent specific commands):**
```bash
bash-ai agent --blacklist "rm,dd,format" "Help me organize my project files"
```

**Specify a different model:**
```bash
# Set in .env file
GEMINI_MODEL=gemini-3-pro-preview
```

### Bash Integration

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# Add bash-ai to PATH if installed locally
export PATH=$PATH:/path/to/bash.ai/.venv/bin

# Create convenient aliases
alias ask='bash-ai ask'
alias agent='bash-ai agent'
```

Then you can use:
```bash
ask "What is Kubernetes?"
agent "Check my git status and show recent commits"
```

### AI-Enhanced Bash Features

The tool provides intelligent command suggestions and auto-completion:

- **Context-aware suggestions**: Based on your current directory and recent commands
- **Error recovery**: Suggests fixes when commands fail
- **Workflow automation**: Helps orchestrate complex multi-step tasks

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-2.0-flash
DEFAULT_BLACKLIST=rm,dd,format,mkfs
```

The `.env` file is automatically loaded when you run the application - no need to `source` it!

Alternatively, you can export it directly in your shell:
```bash
export GOOGLE_API_KEY="your-api-key-here"
bash-ai ask "Hello"
```

## Development

### Prerequisites

- Python 3.12+
- uv (package manager)
- pre-commit (for git hooks)

### Setup

```bash
# Install dependencies
uv sync --dev

# Install pre-commit hooks
uv run pre-commit install
```

### Running Tests

```bash
uv run pytest
```

### Linting

```bash
uv run ruff check .
uv run black --check .
uv run mypy bash_ai
```

### Formatting

```bash
uv run black .
uv run ruff format .
```

## Project Structure

```
bash.ai/
├── bash_ai/              # Main package
│   ├── __init__.py
│   ├── config.py         # Configuration management
│   ├── agents.py         # Agent definitions
│   ├── runner.py         # Agent execution
│   └── cli.py            # CLI interface
├── tests/                # Test files
├── pyproject.toml        # Project configuration
├── .env.example          # Example environment file
├── README.md             # This file
├── CONTRIBUTING.md       # Contribution guidelines
└── LICENSE               # License file
```

## Security Considerations

- **Command Execution**: The agent mode can execute commands. Always review what the agent plans to do before confirming execution.
- **Allowlist/Blacklist**: Use allowlists in production environments to restrict command execution.
- **API Keys**: Never commit your `.env` file or API keys to version control.
- **Permissions**: The agent runs with the same permissions as your user account.

For detailed security information, see [SECURITY.md](SECURITY.md).

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Google ADK](https://github.com/google/adk)
- Uses [Gemini](https://deepmind.google/technologies/gemini/) models

## Roadmap

- [ ] Interactive mode with conversation history
- [ ] Config file for persistent settings
- [ ] Plugin system for custom tools
- [ ] Better command validation and sandboxing
- [ ] Multi-agent orchestration
- [ ] Web UI option
- [ ] Advanced bash completion integration

## Support

- Issues: [GitHub Issues](https://github.com/made-after-dark/bash.ai/issues)
- Discussions: [GitHub Discussions](https://github.com/made-after-dark/bash.ai/discussions)
