"""View registration for Slack app home and modal decorations."""

from slack_bolt.async_app import AsyncApp


def register(app: AsyncApp):
    """Register static Slack views used by the app.

    The project currently builds the App Home view directly in the event handler,
    so this placeholder remains intentionally small.
    """
    pass
