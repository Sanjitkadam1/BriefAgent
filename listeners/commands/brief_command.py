import os
from agent.state import save_pending_brief

# Called by Slack when a user types /brief "EV market trends" in any channel
# validates the topic isn't empty, saves the topic and channel to state, 
# then posts a Block Kit message in the channel with an "Open BriefAgent →" button 
# that deep links to the assistant sidebar
async def brief_command(ack, client, command):
    await ack()

    user_id = command["user_id"]
    channel_id = command["channel_id"]
    topic = command.get("text", "").strip()

    if not topic:
        await client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text="Please provide a topic. Usage: `/brief [topic]`"
        )
        return

    # Save topic + channel to state so assistant thread can pick it up
    save_pending_brief(user_id, topic, channel_id)

    # Post button message in channel
    await client.chat_postMessage(
        channel=channel_id,
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"📊 *BriefAgent* is ready to research *{topic}*\nOpen the assistant to get your brief."
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Open BriefAgent →"},
                        "url": f"https://slack.com/app_redirect?app={os.environ.get('SLACK_APP_ID')}&tab=messages",
                        "action_id": "open_briefagent"
                    }
                ]
            }
        ]
    )