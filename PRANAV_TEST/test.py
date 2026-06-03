from tavily import AsyncTavilyClient
import json

# This import is simply meant for testing, delete it during real development.
import asyncio 

# Enter your API key here during testing.
client = AsyncTavilyClient(TAVILY_API_KEY) 

# This is esentially a function that waits until the user inputs a query and causes this function to run.
async def search_tavily(user_query):
    if (user_query != "") :
        results = await client.search(
            query = user_query,
            max_results = 4, 
            search_depth = "advanced"
        )

        # This lists the tavily response into a organized dictionary of responses.
        formated = [] 
        for r in results["results"]:
            formated.append({
                "title" : r["title"], 
                "url" : r["url"],
                "content" : r["content"][:500]
            })
        print(formated)
        return formated

# This is just for testing, delete this during actual development of code.
asyncio.run(search_tavily("Tesla-SpaceX IPO"))
