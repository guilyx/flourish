"""Agent definitions for bash.ai."""

import os
from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor

from .config import get_settings


def build_agent_instruction(allowed_commands: list[str], blacklisted_commands: list[str]) -> str:
    """Build the instruction for the agent with allowlist/blacklist.

    Args:
        allowed_commands: List of allowed commands
        blacklisted_commands: List of blacklisted commands

    Returns:
        Instruction string for the agent
    """
    instruction = """You are a helpful assistant that can execute terminal commands to help users with complex workflows.

When you need to execute commands, you can use Python code execution to run shell commands via subprocess or os.system.

IMPORTANT SECURITY RULES:
1. Always validate commands before execution
2. Never execute destructive commands without explicit user confirmation
3. Be cautious with commands that modify files or system state
"""

    if allowed_commands:
        instruction += f"\nALLOWED COMMANDS: You may only use these commands: {', '.join(allowed_commands)}\n"

    if blacklisted_commands:
        instruction += f"\nBLACKLISTED COMMANDS: You must NEVER use these commands: {', '.join(blacklisted_commands)}\n"

    instruction += """
When executing commands:
- Use subprocess.run() with shell=True for bash commands
- Always capture and display output
- Handle errors gracefully
- Explain what you're doing before executing commands
- For file operations, be extra careful and confirm with the user if destructive
"""

    return instruction


def get_ask_agent() -> LlmAgent:
    """Create and return the ask agent (no code execution).

    Returns:
        LlmAgent: The configured ask agent without tools
    """
    settings = get_settings()

    # Configure Google AI settings
    if settings.google_api_key:
        os.environ.setdefault("GOOGLE_API_KEY", settings.google_api_key)
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", settings.google_genai_use_vertexai)

    ask_agent = LlmAgent(
        name="bash_ask_agent",
        model=settings.model,
        description="A helpful assistant that answers questions directly without executing commands.",
        instruction="You are a helpful assistant. Answer questions directly and clearly. Do not execute any commands or tools.",
    )

    return ask_agent


def get_agent_agent(
    allowed_commands: list[str] | None = None,
    blacklisted_commands: list[str] | None = None,
) -> LlmAgent:
    """Create and return the agent with code execution capabilities.

    Args:
        allowed_commands: Optional list of allowed commands (overrides default)
        blacklisted_commands: Optional list of blacklisted commands (overrides default)

    Returns:
        LlmAgent: The configured agent with code execution
    """
    settings = get_settings()

    # Configure Google AI settings
    if settings.google_api_key:
        os.environ.setdefault("GOOGLE_API_KEY", settings.google_api_key)
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", settings.google_genai_use_vertexai)

    # Use provided lists or defaults
    allowed = allowed_commands if allowed_commands is not None else settings.default_allowlist
    blacklisted = (
        blacklisted_commands if blacklisted_commands is not None else settings.default_blacklist
    )

    instruction = build_agent_instruction(allowed, blacklisted)

    agent_agent = LlmAgent(
        name="bash_agent",
        model=settings.model,
        code_executor=BuiltInCodeExecutor(),
        description="An agent that can execute terminal commands to help with complex workflows.",
        instruction=instruction,
    )

    return agent_agent
