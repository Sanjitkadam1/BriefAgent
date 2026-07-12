from tavily import AsyncTavilyClient
import json

from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncTavilyClient(os.environ.get("TAVILY_API_KEY"))


async def search_tavily(user_query):
    """Search Tavily for external source material relevant to a user topic.

    The helper trims each result to a consistent preview length so the caller
    can safely embed the content into a prompt without oversized payloads.
    """
    if user_query != "":
        results = await client.search(
            query = user_query,
            max_results = 4, 
            search_depth = "advanced"
        )

        # Normalize the raw Tavily payload into a compact list of dictionaries
        # that is easier to render into the prompt template and logs.
        formated = []
        for r in results["results"]:
            formated.append({
                "title" : r["title"], 
                "url" : r["url"],
                "content" : r["content"][:500]
            })
        # print(formated)
        return formated
