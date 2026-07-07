from logging import Logger
from slack_bolt.context.say.async_say import AsyncSay
from slack_bolt.context.set_suggested_prompts.async_set_suggested_prompts import AsyncSetSuggestedPrompts
from slack_sdk.web.async_client import AsyncWebClient
from agent.state import get_session, start_session, update_session
from agent.research import run_research
import re


REFINEMENT_PROMPTS = [
    {"title": "Focus on risks", "message": "Focus more on the risks and challenges"},
    {"title": "Make it shorter", "message": "Make the brief more concise"},
    {"title": "Slide-ready version", "message": "Convert this into slide-ready bullets"},
    {"title": "Save as Canvas", "message": "Save this brief as a canvas"},
]

EXPORT_BUTTONS = {
    "type": "actions",
    "elements": [
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "Download PDF"},
            "action_id": "save_as_pdf",
            "style": "primary"
        },
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "Download TXT"},
            "action_id": "save_as_txt"
        }
    ]
}

def _to_slack_mrkdwn(text: str) -> str:
    # ## Header → *Header*
    text = re.sub(r'^## (.+)$', r'*\1*', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'*\1*', text, flags=re.MULTILINE)
    # **bold** → *bold*
    text = re.sub(r'\*\*(.*?)\*\*', r'*\1*', text)
    return text

async def handle_assistant_message(
    payload,
    say: AsyncSay,
    client: AsyncWebClient,
    set_suggested_prompts: AsyncSetSuggestedPrompts,
    logger: Logger
):
    try:
        user_id = payload["user"]
        user_message = payload.get("text", "").strip()
        channel_id = payload["channel"]
        thread_ts = payload["thread_ts"]
        action_token = payload.get("assistant_thread", {}).get("action_token")

        session = get_session(user_id)

        # First message — this IS the topic, run full research
        if not session or session.get("brief") is None:
            topic = user_message

            if not session:
                start_session(user_id)

            await say(f"🔍 Researching *{topic}*... give me a moment.")

            await client.assistant_threads_setStatus(
                channel_id=channel_id,
                thread_ts=thread_ts,
                status="Researching..."
            )

            brief = await run_research(
                topic=topic,
                action_token=action_token,
                client=client,
                logger=logger
            )

            update_session(user_id, topic=topic, brief=brief)
            
            await say(_to_slack_mrkdwn(brief))

            await client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                text="Save this brief as a Canvas?",
                blocks=[EXPORT_BUTTONS]
            )


            await set_suggested_prompts(
                prompts=REFINEMENT_PROMPTS,
                title="Refine or save this brief",
            )

        # Subsequent messages — refinement mode
        else:
            await client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                text="⏳ Refining your brief..."
            )

            await client.assistant_threads_setStatus(
                channel_id=channel_id,
                thread_ts=thread_ts,
                status="Refining..."
            )

            refined = await run_research(
                topic=session["topic"],
                action_token=action_token,
                client=client,
                logger=logger,
                existing_brief=session["brief"],
                refinement_request=user_message
            )

            update_session(user_id, brief=refined)

            await client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                text=_to_slack_mrkdwn(refined)
            )


            await client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                text="Download this brief?",
                blocks=[EXPORT_BUTTONS]
)

            await set_suggested_prompts(
                prompts=REFINEMENT_PROMPTS,
                title="Refine or save this brief",
            )

    except Exception as e:
        logger.exception(f"Failed to handle assistant message: {e}")
        await client.chat_postMessage(  # ← use chat_postMessage not say for error too
            channel=channel_id, # type: ignore
            thread_ts=thread_ts, # type: ignore
            text="Something went wrong. Please try again."
        )