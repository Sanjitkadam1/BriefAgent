import asyncio
import logging
import os
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp
from slack_sdk.web.async_client import AsyncWebClient
from slack_bolt.async_app import AsyncAssistant
from listeners import register_listeners

load_dotenv(dotenv_path=".env", override=False)
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

app = AsyncApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    client=AsyncWebClient(
        base_url=os.environ.get("SLACK_API_URL", "https://slack.com/api"),
        token=os.environ.get("SLACK_BOT_TOKEN"),
    ),
)

assistant = AsyncAssistant()
register_listeners(app, assistant)
app.use(assistant)

async def main():
    handler = AsyncSocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    await handler.start_async()

if __name__ == "__main__":
    asyncio.run(main())