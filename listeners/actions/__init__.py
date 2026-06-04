from slack_bolt.async_app import AsyncApp
from .feedback_buttons import handle_feedback_button
from agent.state import get_pending_brief

def register(app: AsyncApp):
    app.action("feedback")(handle_feedback_button)
    app.action("open_briefagent")(handle_open_briefagent)

async def handle_open_briefagent(ack, body, logger):
    await ack()
    logger.info("BriefAgent button clicked")

async def post_brief_to_channel(ack, body, client, logger):
    await ack()
    user_id = body["user"]["id"]
    pending = get_pending_brief(user_id)
    
    if not pending or pending["brief"] is None:
        # brief not ready yet, don't post
        return
    
    # post pending["brief"] to channel