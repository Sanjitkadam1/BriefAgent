from slack_bolt.async_app import AsyncApp, AsyncAssistant
from listeners import actions, events, views, commands

def register_listeners(app: AsyncApp, assistant: AsyncAssistant):
    actions.register(app)
    events.register(app)
    views.register(app)
    commands.register(app)
    events.register_assistant(assistant)