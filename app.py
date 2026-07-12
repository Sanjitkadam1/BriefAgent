import asyncio
import logging
import os
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp
from slack_sdk.web.async_client import AsyncWebClient
from slack_bolt.async_app import AsyncAssistant
from listeners import register_listeners

# Load local secrets and config from .env so development runs against the
# expected Slack, Anthropic, and Tavily credentials without hardcoding them.
load_dotenv(dotenv_path=".env", override=False)
# Keep the default log level at INFO to avoid verbose output during normal runs.
logging.basicConfig(level=logging.INFO)

# Create the shared Bolt app instance and the Slack HTTP client used by all
# listeners and assistant handlers.
app = AsyncApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    client=AsyncWebClient(
        base_url=os.environ.get("SLACK_API_URL", "https://slack.com/api"),
        token=os.environ.get("SLACK_BOT_TOKEN"),
    ),
)

# The assistant runtime is wired into the app separately so message handling
# and response streaming have a dedicated conversation context.
assistant = AsyncAssistant()
register_listeners(app, assistant)
app.use(assistant)


async def main():
    """Start the Slack app over Socket Mode for local development."""
    # Socket Mode keeps the bot connected to Slack without needing a public
    # webhook endpoint, which is the simplest setup for local testing.
    handler = AsyncSocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())