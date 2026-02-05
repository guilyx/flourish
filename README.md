# Flouri

[![PyPI version](https://img.shields.io/pypi/v/flouri.svg)](https://pypi.org/project/flouri/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/flouri)](https://pypi.org/project/flouri/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flouri.svg)](https://pypi.org/project/flouri/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![CI](https://github.com/guilyx/flouri/actions/workflows/ci.yml/badge.svg)](https://github.com/guilyx/flouri/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/guilyx/flourish/graph/badge.svg)](https://codecov.io/gh/guilyx/flourish)

AI-powered terminal: run normal bash commands and get help from an LLM with `?` or `flouri agent "..."`. Commands use an allowlist/blacklist; supports OpenAI, Anthropic, Google, and others via [LiteLLM](https://litellm.ai/).

## Install

**From PyPI (recommended):**

```bash
pip install flouri
```

**From source:**

```bash
git clone https://github.com/guilyx/flouri.git && cd flouri
pip install -e ".[dev]"
```

Set your API key (see [env.example](env.example)):

```bash
# .env or export
export API_KEY=your-key
export MODEL=gpt-4o-mini   # or anthropic/claude-3-sonnet, gemini/gemini-2.0-flash, etc.
```

## Quick start

**TUI (interactive terminal):**

```bash
flouri
# or: flouri tui
```

Then run shell commands as usual; use `? your question` or `Ctrl+A` for AI help.

**CLI (one-off questions / agent runs):**

```bash
flouri agent "List files and show git status"
flouri agent --stream "Explain how Docker networking works"
```

## Usage

- **In the TUI**: type commands; prefix with `?` (or `Ctrl+A`) to ask the AI. Tab completion, history (`↑/↓`), `Ctrl+R` search, `Ctrl+D` exit.
- **Allowlist/blacklist**: AI-executed commands are controlled via config; see `~/.config/flouri/` and [docs/architecture.md](docs/architecture.md).
- **CLI options**: `flouri agent --allowlist "ls,git,find" "..."`, `--blacklist "rm,dd" "..."`, `--stream` for streaming output.

More examples and workflows: see [GitHub Issues](https://github.com/guilyx/flouri/issues) (e.g. [add more run examples](https://github.com/guilyx/flouri/issues/21)).

## Configuration

- **Environment**: `API_KEY`, `MODEL` (see [env.example](env.example)). `.env` in the current directory is loaded automatically.
- **Commands**: allowlist/blacklist in `~/.config/flouri/config.json` (or project `config/`). The agent can manage these via tools.
- **History**: stored in `~/.config/flouri/history`.

## Development

```bash
pip install -e ".[dev]"
pre-commit install
pytest
ruff check . && black --check .
```

See [CONTRIBUTING.md](CONTRIBUTING.md). Docs: [architecture](docs/architecture.md), [plugins](docs/plugins.md), [third-party stack](docs/third-party-libraries.md).

## Security

The agent can run shell commands. Use allowlist/blacklist and do not commit `.env`. Details: [SECURITY.md](SECURITY.md).

## License

Apache 2.0 — [LICENSE](LICENSE).

## Links

- **PyPI**: [pypi.org/project/flouri](https://pypi.org/project/flouri/)
- **Issues**: [github.com/guilyx/flouri/issues](https://github.com/guilyx/flouri/issues)
- **LiteLLM**: [litellm.ai](https://litellm.ai/) · **Google ADK**: [generative-ai-python](https://github.com/google/generative-ai-python)
