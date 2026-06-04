from logging import Logger
from slack_bolt.context.say.async_say import AsyncSay
from slack_sdk.web.async_client import AsyncWebClient
from agent.state import get_pending_brief, update_brief, clear_pending_brief
from agent.research import run_research

# Called by: Slack's Assistant middleware when the user sends any message in the BriefAgent sidebar thread
# checks if this is the first message (brief is None) → runs full research and posts brief + Post button, 
# or if it's a follow-up message → runs refinement with the user's instruction and updates the brief
async def handle_assistant_message(
    payload,
    say: AsyncSay,
    client: AsyncWebClient,
    logger: Logger
):
    try:
        user_id = payload["user"]
        user_message = payload.get("text", "").strip()
        channel_id = payload["channel"]
        thread_ts = payload["thread_ts"]
        action_token = payload.get("assistant_thread", {}).get("action_token")

        pending = get_pending_brief(user_id)

        if not pending:
            await say("Please use `/brief [topic]` in a channel first.")
            return

        brief = pending.get("brief")

        # First message — run full research
        if brief is None:
            await say("⏳ Running research, give me a moment...")

            await client.assistant_threads_setStatus(
                channel_id=channel_id,
                thread_ts=thread_ts,
                status="Researching..."
            )

            brief = await run_research(
                topic=pending["topic"],
                action_token=action_token,
                client=client,
                logger=logger
            )

            update_brief(user_id, brief)
            await say(brief)

            await client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                text="Ready to post?",
                blocks=[
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "Post to channel →"},
                                "action_id": "post_brief_to_channel",
                                "style": "primary",
                                "value": pending["channel_id"]
                            }
                        ]
                    }
                ]
            )

        # Subsequent messages — refinement mode
        else:
            await say("⏳ Refining your brief...")

            await client.assistant_threads_setStatus(
                channel_id=channel_id,
                thread_ts=thread_ts,
                status="Refining..."
            )

            refined = await run_research(
                topic=f"{pending['topic']} — user refinement: {user_message}",
                action_token=action_token,
                client=client,
                logger=logger,
                existing_brief=brief
            )

            update_brief(user_id, refined)
            await say(refined)

    except Exception as e:
        logger.exception(f"Failed to handle assistant message: {e}")
        await say("Something went wrong. Please try again.")