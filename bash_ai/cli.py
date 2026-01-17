"""CLI interface for bash.ai."""

import sys
from typing import Optional

import click
from rich.console import Console
from rich.markdown import Markdown

from .config import get_settings
from .runner import run_agent_sync, run_ask_sync

console = Console()
error_console = Console(file=sys.stderr, style="bold red")


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Bash.ai - AI-powered bash environment enhancement tool."""
    pass


@cli.command()
@click.argument("prompt", required=True)
def ask(prompt: str):
    """Ask the LLM a question (no command execution).

    Example:
        bash-ai ask "What is the difference between git merge and rebase?"
    """
    try:
        console.print("[bold blue]Thinking...[/bold blue]")
        response = run_ask_sync(prompt)
        console.print(Markdown(response))
    except Exception as e:
        error_console.print(f"Error: {e}")
        sys.exit(1)


@cli.command()
@click.argument("prompt", required=True)
@click.option(
    "--allowlist",
    "-a",
    help="Comma-separated list of allowed commands (e.g., 'ls,cd,git')",
    default=None,
)
@click.option(
    "--blacklist",
    "-b",
    help="Comma-separated list of blacklisted commands (e.g., 'rm,dd')",
    default=None,
)
def agent(prompt: str, allowlist: Optional[str], blacklist: Optional[str]):
    """Use agent with command execution capabilities.

    Example:
        bash-ai agent "List all files in the current directory"
        bash-ai agent -a "ls,cd,git" "Check git status"
        bash-ai agent -b "rm,dd" "Help me organize files"
    """
    try:
        # Parse allowlist and blacklist
        allowed_commands = (
            [cmd.strip() for cmd in allowlist.split(",") if cmd.strip()] if allowlist else None
        )
        blacklisted_commands = (
            [cmd.strip() for cmd in blacklist.split(",") if cmd.strip()] if blacklist else None
        )

        console.print("[bold blue]Agent is working...[/bold blue]")
        response = run_agent_sync(
            prompt,
            allowed_commands=allowed_commands,
            blacklisted_commands=blacklisted_commands,
        )
        console.print(Markdown(response))
    except Exception as e:
        error_console.print(f"Error: {e}")
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
