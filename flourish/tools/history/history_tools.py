"""History-related tools for reading command and conversation history."""

import json
from pathlib import Path
from typing import Any

from ...logging import log_tool_call


def read_bash_history(limit: int = 50) -> dict[str, Any]:
    """
    Read bash command history from the Flourish history file.

    This tool allows the agent to see what bash commands have been executed previously,
    which can help understand user workflow and context.

    Args:
        limit: Maximum number of history entries to return (default: 50, max: 1000).

    Returns:
        A dictionary with status, history entries, and count.
    """
    history_file = Path.home() / ".config" / "flourish" / "history"

    # Validate limit
    if limit < 1:
        limit = 1
    if limit > 1000:
        limit = 1000

    result: dict[str, Any] = {
        "status": "success",
        "history_file": str(history_file),
        "entries": [],
        "count": 0,
    }

    try:
        if not history_file.exists():
            result["message"] = "History file does not exist yet"
            log_tool_call("read_bash_history", {"limit": limit}, result, success=True)
            return result

        # Read history file (prompt-toolkit FileHistory format: one command per line)
        with open(history_file, encoding="utf-8") as f:
            lines = f.readlines()

        # Filter out empty lines and get unique commands (most recent first)
        commands = []
        seen = set()
        for line in reversed(lines):  # Start from most recent
            cmd = line.strip()
            if cmd and cmd not in seen:
                commands.append(cmd)
                seen.add(cmd)
                if len(commands) >= limit:
                    break

        # Reverse to show oldest first (or keep newest first - let's keep newest first)
        result["entries"] = commands
        result["count"] = len(commands)
        result["message"] = f"Retrieved {len(commands)} history entries"

    except PermissionError:
        result["status"] = "error"
        result["message"] = "Permission denied reading history file"
        log_tool_call("read_bash_history", {"limit": limit}, result, success=False)
        return result
    except Exception as e:
        result["status"] = "error"
        result["message"] = f"Error reading history: {str(e)}"
        log_tool_call("read_bash_history", {"limit": limit}, result, success=False)
        return result

    log_tool_call("read_bash_history", {"limit": limit}, result, success=True)
    return result


def read_conversation_history(limit: int = 20) -> dict[str, Any]:
    """
    Read conversation history from the most recent Flourish session log.

    This tool allows the agent to see previous conversations, tool calls, and events
    from the current or most recent session, helping maintain context across interactions.

    Args:
        limit: Maximum number of log entries to return (default: 20, max: 100).

    Returns:
        A dictionary with status, log entries, session info, and count.
    """
    logs_dir = Path.home() / ".config" / "flourish" / "logs"

    # Validate limit
    if limit < 1:
        limit = 1
    if limit > 100:
        limit = 100

    result: dict[str, Any] = {
        "status": "success",
        "session_dir": None,
        "entries": [],
        "count": 0,
    }

    try:
        if not logs_dir.exists():
            result["message"] = "Logs directory does not exist yet"
            log_tool_call("read_conversation_history", {"limit": limit}, result, success=True)
            return result

        # Find most recent session directory
        session_dirs = sorted(
            [d for d in logs_dir.iterdir() if d.is_dir() and d.name.startswith("session_")],
            key=lambda x: x.stat().st_mtime,
            reverse=True,
        )

        if not session_dirs:
            result["message"] = "No session logs found"
            log_tool_call("read_conversation_history", {"limit": limit}, result, success=True)
            return result

        # Use most recent session
        latest_session = session_dirs[0]
        conversation_log = latest_session / "conversation.log"

        if not conversation_log.exists():
            result["message"] = "Conversation log file does not exist"
            log_tool_call("read_conversation_history", {"limit": limit}, result, success=True)
            return result

        result["session_dir"] = str(latest_session)

        # Read and parse log entries
        # Format: "timestamp - name - level - JSON_MESSAGE"
        entries = []
        with open(conversation_log, encoding="utf-8") as f:
            lines = f.readlines()

        # Parse entries from most recent first
        for line in reversed(lines[-limit * 2 :]):  # Read more lines to account for formatting
            line = line.strip()
            if not line:
                continue

            # Parse log format: "timestamp - name - level - JSON_MESSAGE"
            # Try to extract JSON part (after the third " - ")
            parts = line.split(" - ", 3)
            if len(parts) >= 4:
                try:
                    log_data = json.loads(parts[3])
                    entries.append(
                        {
                            "timestamp": log_data.get("timestamp", parts[0]),
                            "event": log_data.get("event", "unknown"),
                            "data": log_data,
                        }
                    )
                    if len(entries) >= limit:
                        break
                except json.JSONDecodeError:
                    # Skip malformed entries
                    continue

        # Reverse to show oldest first (chronological order)
        entries.reverse()
        result["entries"] = entries
        result["count"] = len(entries)
        result["message"] = (
            f"Retrieved {len(entries)} conversation log entries from {latest_session.name}"
        )

    except PermissionError:
        result["status"] = "error"
        result["message"] = "Permission denied reading conversation logs"
        log_tool_call("read_conversation_history", {"limit": limit}, result, success=False)
        return result
    except Exception as e:
        result["status"] = "error"
        result["message"] = f"Error reading conversation history: {str(e)}"
        log_tool_call("read_conversation_history", {"limit": limit}, result, success=False)
        return result

    log_tool_call("read_conversation_history", {"limit": limit}, result, success=True)
    return result
