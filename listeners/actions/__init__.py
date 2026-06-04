from slack_bolt.async_app import AsyncApp
from .feedback_buttons import handle_feedback_button

def register(app: AsyncApp):
    app.action("feedback")(handle_feedback_button)
    app.action("open_briefagent")(handle_open_briefagent)

async def handle_open_briefagent(ack, body, logger):
    await ack()
    logger.info("BriefAgent button clicked")