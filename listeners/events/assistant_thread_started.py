"""Initialize the assistant thread with a clean state and starter prompt ideas."""

from logging import Logger
from slack_bolt.context.set_suggested_prompts.async_set_suggested_prompts import AsyncSetSuggestedPrompts
from slack_bolt.context.say.async_say import AsyncSay
from agent.state import clear_session

SUGGESTED_PROMPTS = [
    {"title": "NVIDIA market trends", "message": "NVIDIA market trends"},
    {"title": "Fed rate decision", "message": "Fed rate decision impact"},
    {"title": "EV market overview", "message": "EV market overview"},
]


async def handle_assistant_thread_started(
    payload,
    set_suggested_prompts: AsyncSetSuggestedPrompts,
    say: AsyncSay,
    logger: Logger,
):
    """Reset per-user state when a new assistant thread starts."""
    try:
        user_id = payload["assistant_thread"]["user_id"]

        clear_session(user_id)

        await say("What would you like a research brief on?")
        await set_suggested_prompts(prompts=SUGGESTED_PROMPTS, title="Try one of these, or type your own topic")


    except Exception as e:
        logger.exception(f"Failed to handle assistant thread started: {e}")
        await say("Something went wrong. Please try again.")