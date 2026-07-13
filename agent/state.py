"""Small in-memory session cache for the assistant thread flow.

The structure keeps the current topic and most recent brief per user so the
assistant can refine a single ongoing brief without needing a database.
"""

# In-memory session store: { user_id: { "topic": str, "brief": str | None } }
sessions = {}


def get_session(user_id: str):
    """Return the in-memory state for a single user, if one exists."""
    return sessions.get(user_id)


def start_session(user_id: str):
    """Initialize the per-user session container for a fresh research thread."""
    sessions[user_id] = {
        "topic": None,
        "brief": None,
    }


def update_session(user_id: str, **kwargs):
    """Merge new state fields into the existing session for the user."""
    if user_id not in sessions:
        sessions[user_id] = {"topic": None, "brief": None}
    sessions[user_id].update(kwargs)


def clear_session(user_id: str):
    """Remove a user's session when a new assistant thread begins."""
    if user_id in sessions:
        del sessions[user_id]