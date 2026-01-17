"""Runner for executing agent interactions."""

import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .agents import get_ask_agent, get_agent_agent
from .config import get_settings


async def run_ask_agent(prompt: str) -> str:
    """Run the ask agent with a prompt.

    Args:
        prompt: The user's prompt

    Returns:
        The agent's response text
    """
    settings = get_settings()
    agent = get_ask_agent()

    # Create session
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=settings.app_name,
        user_id=settings.user_id,
        session_id=settings.session_id_ask,
    )

    # Create runner
    runner = Runner(agent=agent, app_name=settings.app_name, session_service=session_service)

    # Create user content
    content = types.Content(role="user", parts=[types.Part(text=prompt)])

    final_response_text = ""

    try:
        async for event in runner.run_async(
            user_id=settings.user_id,
            session_id=settings.session_id_ask,
            new_message=content,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text and not part.text.isspace():
                        final_response_text = part.text.strip()

            if event.is_final_response():
                if event.content and event.content.parts and event.content.parts[0].text:
                    final_response_text = event.content.parts[0].text.strip()
                    break

    except Exception as e:
        raise RuntimeError(f"Error during agent run: {e}") from e

    return final_response_text


async def run_agent_agent(
    prompt: str,
    allowed_commands: list[str] | None = None,
    blacklisted_commands: list[str] | None = None,
) -> str:
    """Run the agent with code execution capabilities.

    Args:
        prompt: The user's prompt
        allowed_commands: Optional list of allowed commands
        blacklisted_commands: Optional list of blacklisted commands

    Returns:
        The agent's response text
    """
    settings = get_settings()
    agent = get_agent_agent(
        allowed_commands=allowed_commands,
        blacklisted_commands=blacklisted_commands,
    )

    # Create session
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=settings.app_name,
        user_id=settings.user_id,
        session_id=settings.session_id_agent,
    )

    # Create runner
    runner = Runner(agent=agent, app_name=settings.app_name, session_service=session_service)

    # Create user content
    content = types.Content(role="user", parts=[types.Part(text=prompt)])

    final_response_text = ""
    output_lines = []

    try:
        async for event in runner.run_async(
            user_id=settings.user_id,
            session_id=settings.session_id_agent,
            new_message=content,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.executable_code:
                        output_lines.append(f"Code: {part.executable_code.code}")
                    elif part.code_execution_result:
                        output_lines.append(
                            f"Execution Result: {part.code_execution_result.outcome}\n"
                            f"Output: {part.code_execution_result.output}"
                        )
                    elif part.text and not part.text.isspace():
                        final_response_text = part.text.strip()

            if event.is_final_response():
                if event.content and event.content.parts and event.content.parts[0].text:
                    final_response_text = event.content.parts[0].text.strip()

    except Exception as e:
        raise RuntimeError(f"Error during agent run: {e}") from e

    # Combine output
    if output_lines:
        return "\n".join(output_lines) + "\n\n" + final_response_text

    return final_response_text


def run_ask_sync(prompt: str) -> str:
    """Synchronous wrapper for run_ask_agent.

    Args:
        prompt: The user's prompt

    Returns:
        The agent's response text
    """
    return asyncio.run(run_ask_agent(prompt))


def run_agent_sync(
    prompt: str,
    allowed_commands: list[str] | None = None,
    blacklisted_commands: list[str] | None = None,
) -> str:
    """Synchronous wrapper for run_agent_agent.

    Args:
        prompt: The user's prompt
        allowed_commands: Optional list of allowed commands
        blacklisted_commands: Optional list of blacklisted commands

    Returns:
        The agent's response text
    """
    return asyncio.run(
        run_agent_agent(
            prompt,
            allowed_commands=allowed_commands,
            blacklisted_commands=blacklisted_commands,
        )
    )
