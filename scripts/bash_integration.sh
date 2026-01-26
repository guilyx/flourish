#!/bin/bash
# Bash integration script for Flourish
# Add this to your ~/.bashrc or ~/.zshrc

# Function to provide AI-powered command suggestions
_bash_ai_suggest() {
    local command="$1"
    if [ -z "$command" ]; then
        return
    fi

    # Check if flourish is available
    if ! command -v flourish &> /dev/null; then
        return
    fi

    # Get AI suggestion (non-blocking, runs in background)
    (flourish "Suggest the next command after: $command" 2>/dev/null) &
}

# Function to enhance command execution with AI
_bash_ai_enhance() {
    local last_command="$1"
    local exit_code="$2"

    # If command failed, ask AI for help
    if [ "$exit_code" -ne 0 ]; then
        if command -v flourish &> /dev/null; then
            echo ""
            echo "💡 AI Suggestion:"
            flourish "The command '$last_command' failed with exit code $exit_code. What might be wrong and how to fix it?" 2>/dev/null | head -5
            echo ""
        fi
    fi
}

# Hook into command execution (if supported)
if [ -n "$BASH_VERSION" ]; then
    # Bash-specific hooks
    trap '_bash_ai_enhance "$BASH_COMMAND" "$?"' DEBUG 2>/dev/null || true
fi

# Create convenient alias
alias ai='flourish'

# Auto-completion helper
_bash_ai_complete() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    if [ "$COMP_CWORD" -eq 1 ]; then
        COMPREPLY=($(compgen -W "--allowlist --blacklist --help --version" -- "$cur"))
    fi
}

# Register completion (if available)
if command -v complete &> /dev/null; then
    complete -F _bash_ai_complete flourish
fi

echo "Flourish integration loaded. Use 'flourish' or 'ai' command."
