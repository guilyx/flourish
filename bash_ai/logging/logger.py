"""Logging utilities for bash.ai."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

# Configure logs directory
LOGS_DIR = Path.home() / ".config" / "bash.ai" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Global logger instance and log file
_logger: logging.Logger | None = None
_log_file: Path | None = None


def initialize_session_log() -> Path:
    """Initialize the session log file at the beginning of a session.

    Creates a new log file with timestamp and logs session start.

    Returns:
        Path to the created log file.
    """
    global _logger, _log_file

    # Create new log file with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    _log_file = LOGS_DIR / f"session_{timestamp}.log"

    # Reset logger to create new handler
    _logger = None

    logger = _setup_logger()

    session_start = {
        "timestamp": datetime.now().isoformat(),
        "event": "session_start",
        "message": "Bash.ai session started",
    }

    logger.info(json.dumps(session_start))

    return _log_file


def _setup_logger() -> logging.Logger:
    """Set up the logger for tool calls and conversations.

    Returns:
        Configured logger instance.
    """
    global _logger, _log_file

    # Return existing logger if already set up
    if _logger is not None and _logger.handlers:
        return _logger

    # Create logger
    logger = logging.getLogger("bash_ai")
    logger.setLevel(logging.INFO)

    # Clear any existing handlers
    logger.handlers.clear()

    # Use existing log file or create new one
    if _log_file is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        _log_file = LOGS_DIR / f"session_{timestamp}.log"

    # Create file handler
    file_handler = logging.FileHandler(_log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    _logger = logger

    return logger


def log_tool_call(
    tool_name: str,
    parameters: dict[str, Any],
    result: Any,
    success: bool = True,
) -> None:
    """Log a tool call to the log file.

    Args:
        tool_name: Name of the tool that was called
        parameters: Dictionary of parameters passed to the tool
        result: Result returned by the tool (will be converted to string)
        success: Whether the tool call was successful
    """
    logger = _setup_logger()

    # Convert result to string, truncating if too long
    result_str = str(result)
    if len(result_str) > 1000:
        result_str = result_str[:1000] + "... [truncated]"

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": "tool_call",
        "tool": tool_name,
        "parameters": parameters,
        "result": result_str,
        "success": success,
    }

    # Log as JSON for easy parsing
    try:
        logger.info(json.dumps(log_entry))
    except Exception as e:
        # Fallback to basic logging if JSON serialization fails
        logger.warning(f"Failed to log tool call as JSON: {e}")
        logger.info(f"Tool: {tool_name}, Success: {success}, Params: {parameters}")


def log_conversation(
    role: str,
    content: str,
    metadata: dict[str, Any] | None = None,
) -> None:
    """Log a conversation message (user or agent).

    Args:
        role: Role of the speaker ('user' or 'agent')
        content: The message content
        metadata: Optional additional metadata to include
    """
    logger = _setup_logger()

    # Truncate long messages
    content_str = content
    if len(content_str) > 2000:
        content_str = content_str[:2000] + "... [truncated]"

    log_entry: dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "event": "conversation",
        "role": role,
        "content": content_str,
    }

    if metadata:
        log_entry["metadata"] = metadata

    # Log as JSON for easy parsing
    try:
        logger.info(json.dumps(log_entry))
    except Exception as e:
        # Fallback to basic logging if JSON serialization fails
        logger.warning(f"Failed to log conversation as JSON: {e}")
        logger.info(f"Conversation - {role}: {content_str[:100]}")


def log_session_end() -> None:
    """Log session end."""
    logger = _setup_logger()

    session_end = {
        "timestamp": datetime.now().isoformat(),
        "event": "session_end",
        "message": "Bash.ai session ended",
    }

    logger.info(json.dumps(session_end))
