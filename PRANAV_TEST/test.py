from tavily import AsyncTavilyClient
import json
import asyncio 
#enter API key here 
client = AsyncTavilyClient("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") 


async def search_tavily(user_query):
    if (user_query != "") :
        results = await client.search(
            query = user_query,
            max_results = 4, 
            search_depth = "advanced"
        )

        #package lists intoa  cleanly organized dictionary
        formated = [] 
        for r in results["results"]:
            formated.append({
                "title" : r["title"], 
                "url" : r["url"],
                "content" : r["content"][:500]
            })
        print(formated)
        return formated

asyncio.run(search_tavily("Tesla-SpaceX IPO"))