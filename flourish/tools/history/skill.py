"""History management skill."""

from ..base import BaseSkill, FunctionToolWrapper
from .history_tools import read_bash_history, read_conversation_history


class HistorySkill(BaseSkill):
    """History management skill."""

    def __init__(self):
        """Initialize the history skill."""
        super().__init__(
            name="history",
            description="History-related tools for reading command and conversation history",
            tools=[
                FunctionToolWrapper(
                    "read_bash_history",
                    read_bash_history,
                    "Read bash command history",
                ),
                FunctionToolWrapper(
                    "read_conversation_history",
                    read_conversation_history,
                    "Read conversation history",
                ),
            ],
        )
