from slack_bolt.async_app import AsyncApp
from .feedback_buttons import handle_feedback_button
from agent.state import get_session
from agent.pdfexport import upload_brief_as_pdf
from agent.txtexport import upload_brief_as_txt

def register(app: AsyncApp):
    app.action("feedback")(handle_feedback_button)
    app.action("save_as_pdf")(handle_save_as_pdf)
    app.action("save_as_txt")(handle_save_as_txt)


async def handle_save_as_pdf(ack, body, client, logger):
    await ack()
    try:
        user_id = body["user"]["id"]
        channel_id = body["container"]["channel_id"]  # ← already the DM channel
        session = get_session(user_id)

        if not session or not session.get("brief"):
            return

        await upload_brief_as_pdf(
            client=client,
            channel_id=channel_id,
            topic=session["topic"],
            brief=session["brief"],
            logger=logger
        )

        await client.chat_postMessage(
            channel=channel_id,
            thread_ts=body["container"]["message_ts"],
            text="Your brief has been sent — check the *History* tab above to download it."
        )

    except Exception as e:
        logger.exception(f"Failed to save as PDF: {e}")


async def handle_save_as_txt(ack, body, client, logger):
    await ack()
    try:
        user_id = body["user"]["id"]
        channel_id = body["container"]["channel_id"]  # ← already the DM channel
        session = get_session(user_id)

        if not session or not session.get("brief"):
            return

        await upload_brief_as_txt(
            client=client,
            channel_id=channel_id,
            topic=session["topic"],
            brief=session["brief"],
            logger=logger
        )

        await client.chat_postMessage(
            channel=channel_id,
            thread_ts=body["container"]["message_ts"],
            text="Your brief has been sent — check the *History* tab above to download it."
        )

    except Exception as e:
        logger.exception(f"Failed to save as TXT: {e}")