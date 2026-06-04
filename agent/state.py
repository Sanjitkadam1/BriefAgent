# In-memory store: { user_id: { "topic": str, "channel_id": str, "brief": str } }
pending_briefs = {}

# Called by the /brief command handler
# Saves the user's topic and channel into the dict so the assistant thread can retrieve it later
def save_pending_brief(user_id: str, topic: str, channel_id: str):
    pending_briefs[user_id] = {
        "topic": topic,
        "channel_id": channel_id,
        "brief": None
    }

# Called by: assistant_thread_started.py when the sidebar opens
# looks up the topic and channel for a given user so the assistant knows what to research
def get_pending_brief(user_id: str):
    return pending_briefs.get(user_id)

# Called by: assistant_thread_started.py and message.py after Claude generates or refines a brief
# Overwrites the stored brief with the latest version so we always have the most current draft ready to post
def update_brief(user_id: str, brief: str):
    if user_id in pending_briefs:
        pending_briefs[user_id]["brief"] = brief

# Called by: the "Post to #channel" button handler after the brief gets posted
# Deletes the user's entry from the dict to clean up state so stale data doesn't carry over to their next /brief call
def clear_pending_brief(user_id: str):
    if user_id in pending_briefs:
        del pending_briefs[user_id]