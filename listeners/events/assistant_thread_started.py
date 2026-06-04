from logging import Logger
from slack_bolt.context.set_suggested_prompts.async_set_suggested_prompts import AsyncSetSuggestedPrompts
from slack_bolt.context.say.async_say import AsyncSay
from slack_sdk.web.async_client import AsyncWebClient
from agent.state import get_pending_brief, update_brief
from agent.research import run_research

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
    client: AsyncWebClient,
    logger: Logger
):
    try:
        user_id = payload["assistant_thread"]["user_id"]
        channel_id = payload["assistant_thread"]["channel_id"]
        thread_ts = payload["assistant_thread"]["thread_ts"]

        await set_suggested_prompts(
            prompts=SUGGESTED_PROMPTS,
            title="What would you like to do with your brief?",
        )

        pending = get_pending_brief(user_id)

        if not pending:
            await say("Hi! Use `/brief [topic]` in any channel to get started.")
            return

        topic = pending["topic"]
        origin_channel = pending["channel_id"]

        await say(f"🔍 Researching *{topic}*... give me a moment.")

        await client.assistant_threads_setStatus(
            channel_id=channel_id,
            thread_ts=thread_ts,
            status="Researching your topic..."
        )

        brief = await run_research(
            topic=topic,
            user_id=user_id,
            channel_id=channel_id,
            thread_ts=thread_ts,
            client=client,
            logger=logger
        )

        update_brief(user_id, brief)
        await say(brief)

        await client.chat_postMessage(
            channel=channel_id,
            thread_ts=thread_ts,
            blocks=[
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Post to channel →"},
                            "action_id": "post_brief_to_channel",
                            "style": "primary",
                            "value": origin_channel
                        }
                    ]
                }
            ]
        )

    except Exception as e:
        logger.exception(f"Failed to handle assistant thread started: {e}")
        await say("Something went wrong while researching. Please try again.")