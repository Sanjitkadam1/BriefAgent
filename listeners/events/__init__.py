"""Event registration for Slack app lifecycle and message hooks."""

from slack_bolt.async_app import AsyncApp, AsyncAssistant
from .app_home_opened import handle_app_home_opened
from .app_mentioned import handle_app_mentioned
from .assistant_thread_started import handle_assistant_thread_started
from .message import handle_message
from .assistant_message import handle_assistant_message


def register(app: AsyncApp):
    """Wire the standard Slack app events to their handler functions."""
    app.event("app_home_opened")(handle_app_home_opened)
    app.event("app_mention")(handle_app_mentioned)
    app.event("message")(handle_message)


def register_assistant(assistant: AsyncAssistant):
    """Wire assistant-thread callbacks used by the Claude SDK conversation flow."""
    assistant.thread_started(handle_assistant_thread_started)
    assistant.user_message(handle_assistant_message)
