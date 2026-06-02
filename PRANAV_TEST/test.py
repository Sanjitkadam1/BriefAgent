from tavily import TavilyClient
import os

tavily = TavilyClient(api_key="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")
results = tavily.search(query="EV market trends 2026", max_results=3)

for r in results["results"]:
    print(r["title"])
    print(r["url"])
    print(r["content"][:200])
    print("---")
