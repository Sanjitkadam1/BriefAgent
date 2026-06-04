from logging import Logger
from slack_bolt.context.set_suggested_prompts.async_set_suggested_prompts import AsyncSetSuggestedPrompts
from slack_bolt.context.say.async_say import AsyncSay
from agent.state import get_pending_brief

SUGGESTED_PROMPTS = [
    {"title": "Focus on risks", "message": "Focus more on the risks and challenges"},
    {"title": "Make it shorter", "message": "Make the brief more concise"},
    {"title": "Add competitors", "message": "Add a section on key competitors"},
    {"title": "Post to channel", "message": "Post this brief to the channel"},
]

async def handle_assistant_thread_started(
    payload,
    set_suggested_prompts: AsyncSetSuggestedPrompts,
    say: AsyncSay,
    logger: Logger
):
    try:
        user_id = payload["assistant_thread"]["user_id"]

        await set_suggested_prompts(
            prompts=SUGGESTED_PROMPTS,
            title="What would you like to do with your brief?",
        )

        pending = get_pending_brief(user_id)

        if not pending:
            await say("Hi! Use `/brief [topic]` in any channel to get started.")
            return

        topic = pending["topic"]
        await say(f"🔍 Ready to research *{topic}*.\nSend any message to begin.")

    except Exception as e:
        logger.exception(f"Failed to handle assistant thread started: {e}")
        await say("Something went wrong. Please try again.")