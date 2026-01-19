"""Runner for executing agent interactions using LiteLLM."""

import asyncio
import json
from typing import Any

from ..agent import get_agent
from ..config import get_settings
from ..logging import initialize_session_log, log_conversation
from ..tools import (
    add_to_allowlist,
    add_to_blacklist,
    execute_bash,
    list_allowlist,
    list_blacklist,
    remove_from_allowlist,
    remove_from_blacklist,
    set_cwd,
)

# Tool mapping for function calling
TOOL_FUNCTIONS = {
    "set_cwd": set_cwd,
    "execute_bash": execute_bash,
    "add_to_allowlist": add_to_allowlist,
    "remove_from_allowlist": remove_from_allowlist,
    "add_to_blacklist": add_to_blacklist,
    "remove_from_blacklist": remove_from_blacklist,
    "list_allowlist": list_allowlist,
    "list_blacklist": list_blacklist,
}


def execute_tool(tool_name: str, arguments: dict[str, Any]) -> Any:
    """Execute a tool function.

    Args:
        tool_name: Name of the tool to execute
        arguments: Arguments for the tool

    Returns:
        Result from the tool execution
    """
    if tool_name not in TOOL_FUNCTIONS:
        return {"status": "error", "message": f"Unknown tool: {tool_name}"}

    tool_func = TOOL_FUNCTIONS[tool_name]

    # Handle tools that don't need ToolContext
    if tool_name in ["set_cwd", "list_allowlist", "list_blacklist"]:
        return tool_func(**arguments)

    # For tools that need ToolContext, pass None (they'll auto-confirm in LiteLLM mode)
    tool_context = None

    # Call tool with context
    try:
        if tool_name == "execute_bash":
            return tool_func(arguments["cmd"], tool_context)
        elif tool_name in ["add_to_allowlist", "remove_from_allowlist", "add_to_blacklist", "remove_from_blacklist"]:
            return tool_func(arguments["command"], tool_context)
        else:
            # For tools that don't need tool_context, just pass arguments
            return tool_func(**arguments)
    except Exception as e:
        return {"status": "error", "message": f"Tool execution error: {e}"}


async def run_agent(
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
    # Initialize session log if not already done
    initialize_session_log()

    # Log user message
    log_conversation("user", prompt)

    # Get agent function and tools
    agent_func = get_agent(
        allowed_commands=allowed_commands,
        blacklisted_commands=blacklisted_commands,
    )

    from ..tools import get_bash_tools_dict

    tools = get_bash_tools_dict(allowlist=allowed_commands, blacklist=blacklisted_commands)

    # Initial messages
    messages = [{"role": "user", "content": prompt}]

    max_iterations = 10  # Prevent infinite loops
    iteration = 0
    full_response = ""

    while iteration < max_iterations:
        iteration += 1

        # Call agent
        response = agent_func(messages, tools=tools)

        # Check for tool calls
        if response.choices and response.choices[0].message.tool_calls:
            # Execute tools
            tool_results = []
            for tool_call in response.choices[0].message.tool_calls:
                tool_name = tool_call.function.name
                try:
                    arguments = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    arguments = {}

                result = execute_tool(tool_name, arguments)

                tool_results.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": tool_name,
                        "content": json.dumps(result),
                    }
                )

            # Add tool results to messages
            messages.append(response.choices[0].message)
            messages.extend(tool_results)

            # Continue loop to get next response
            continue

        # No tool calls - we have final response
        if response.choices and response.choices[0].message.content:
            full_response = response.choices[0].message.content
            break

    # Log agent response
    log_conversation("agent", full_response)

    return full_response


async def run_agent_live(
    prompt: str,
    allowed_commands: list[str] | None = None,
    blacklisted_commands: list[str] | None = None,
    stream_callback=None,
) -> str:
    """Run the agent with live streaming output.

    Args:
        prompt: The user's prompt
        allowed_commands: Optional list of allowed commands
        blacklisted_commands: Optional list of blacklisted commands
        stream_callback: Optional callback function(text) called for each text chunk

    Returns:
        The complete agent's response text
    """
    # Initialize session log if not already done
    initialize_session_log()

    # Log user message
    log_conversation("user", prompt)

    # Get agent function and tools
    agent_func = get_agent(
        allowed_commands=allowed_commands,
        blacklisted_commands=blacklisted_commands,
    )

    from ..tools import get_bash_tools_dict

    tools = get_bash_tools_dict(allowlist=allowed_commands, blacklist=blacklisted_commands)

    # Initial messages
    messages = [{"role": "user", "content": prompt}]

    max_iterations = 10
    iteration = 0
    full_response = ""

    while iteration < max_iterations:
        iteration += 1

        # Call agent with streaming
        settings = get_settings()
        from litellm import completion

        response_stream = completion(
            model=settings.model,
            messages=messages,
            tools=tools,
            api_key=settings.api_key,
            api_base=settings.api_base,
            stream=True,
        )

        # Process streaming response
        current_message = {"role": "assistant", "content": "", "tool_calls": []}
        tool_calls = []

        for chunk in response_stream:
            if chunk.choices and chunk.choices[0].delta:
                delta = chunk.choices[0].delta

                # Handle content streaming
                if delta.content:
                    full_response += delta.content
                    if stream_callback:
                        stream_callback(delta.content)

                # Handle tool calls
                if delta.tool_calls:
                    for tool_call_delta in delta.tool_calls:
                        idx = tool_call_delta.index
                        if idx >= len(tool_calls):
                            tool_calls.extend([None] * (idx + 1 - len(tool_calls)))
                        if tool_calls[idx] is None:
                            tool_calls[idx] = {
                                "id": tool_call_delta.id,
                                "type": "function",
                                "function": {"name": "", "arguments": ""},
                            }
                        if tool_call_delta.function:
                            if tool_call_delta.function.name:
                                tool_calls[idx]["function"]["name"] = tool_call_delta.function.name
                            if tool_call_delta.function.arguments:
                                tool_calls[idx]["function"]["arguments"] += tool_call_delta.function.arguments

        # If we have tool calls, execute them
        if tool_calls:
            current_message["tool_calls"] = tool_calls
            messages.append(current_message)

            # Execute tools
            tool_results = []
            for tool_call in tool_calls:
                tool_name = tool_call["function"]["name"]
                try:
                    arguments = json.loads(tool_call["function"]["arguments"])
                except json.JSONDecodeError:
                    arguments = {}

                result = execute_tool(tool_name, arguments)

                tool_results.append(
                    {
                        "tool_call_id": tool_call["id"],
                        "role": "tool",
                        "name": tool_name,
                        "content": json.dumps(result),
                    }
                )

            messages.extend(tool_results)
            continue

        # No tool calls - we're done
        if full_response:
            break

    # Log agent response
    log_conversation("agent", full_response)

    return full_response


def run_agent_sync(
    prompt: str,
    allowed_commands: list[str] | None = None,
    blacklisted_commands: list[str] | None = None,
) -> str:
    """Synchronous wrapper for run_agent.

    Args:
        prompt: The user's prompt
        allowed_commands: Optional list of allowed commands
        blacklisted_commands: Optional list of blacklisted commands

    Returns:
        The agent's response text
    """
    return asyncio.run(
        run_agent(
            prompt,
            allowed_commands=allowed_commands,
            blacklisted_commands=blacklisted_commands,
        )
    )


def run_agent_live_sync(
    prompt: str,
    allowed_commands: list[str] | None = None,
    blacklisted_commands: list[str] | None = None,
    stream_callback=None,
) -> str:
    """Synchronous wrapper for run_agent_live.

    Args:
        prompt: The user's prompt
        allowed_commands: Optional list of allowed commands
        blacklisted_commands: Optional list of blacklisted commands
        stream_callback: Optional callback function(text) called for each text chunk

    Returns:
        The complete agent's response text
    """
    return asyncio.run(
        run_agent_live(
            prompt,
            allowed_commands=allowed_commands,
            blacklisted_commands=blacklisted_commands,
            stream_callback=stream_callback,
        )
    )
