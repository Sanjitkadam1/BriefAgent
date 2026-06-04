from logging import Logger
from slack_bolt.context.say.async_say import AsyncSay

async def handle_assistant_message(
    payload,
    say: AsyncSay,
    logger: Logger
):
    try:
        user_message = payload.get("text", "")
        logger.info(f"User said: {user_message}")
        await say(f"Got your message: {user_message} (refinement logic coming soon)")
    except Exception as e:
        logger.exception(f"Failed to handle assistant message: {e}")