# In-memory session store: { user_id: { "topic": str, "brief": str | None } }
sessions = {}

def get_session(user_id: str):
    return sessions.get(user_id)

def start_session(user_id: str):
    sessions[user_id] = {
        "topic": None,
        "brief": None
    }

def update_session(user_id: str, **kwargs):
    if user_id not in sessions:
        sessions[user_id] = {"topic": None, "brief": None}
    sessions[user_id].update(kwargs)

def clear_session(user_id: str):
    if user_id in sessions:
        del sessions[user_id]