from slack_bolt.async_app import AsyncApp
from .brief_command import brief_command

def register(app: AsyncApp):
    app.command("/brief")(brief_command)