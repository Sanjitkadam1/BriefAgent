import os
import time
import anthropic
from datetime import date
from search import search_tavily

# Load prompts once at module level
def _load_prompt(filename):
    path = os.path.join("prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

SYSTEM_PROMPT = _load_prompt("system_prompt.txt")
USER_TEMPLATE = _load_prompt("user_prompt.txt")
REFINEMENT_TEMPLATE = _load_prompt("refinement_prompt.txt")


async def run_research(topic, action_token, client, logger, existing_brief=None, refinement_request=None):
    timings = {}
    try:
        # Step 1 — RTS API: pull internal Slack context
        t0 = time.perf_counter()
        rts_results = ""
        if action_token:
            try:
                rts_response = await client.api_call(
                    "assistant.search.context",
                    json={
                        "action_token": action_token,
                        "query": topic
                    }
                )
                messages = rts_response.get("results", {}).get("messages", [])
                if messages:
                    rts_results = "\n".join([
                        f"- {m.get('content', '')}" for m in messages[:10] if m.get('content')
                    ])
                    logger.info(f"RTS returned {len(messages)} messages")
                else:
                    rts_results = "No relevant internal messages found."
            except Exception as e:
                logger.warning(f"RTS API call failed: {e}")
                rts_results = "Internal search unavailable."
        timings["rts"] = time.perf_counter() - t0
        logger.info(f"Timing — RTS: {timings['rts']:.2f}s")

        # Step 2 — Tavily: pull external web data
        t1 = time.perf_counter()
        tavily_results = ""
        sources = "External search unavailable"
        try:
            results = await search_tavily(topic)
            if results:
                tavily_results = "\n".join([
                    f"- *{r['title']}* ({r['url']})\n  {r['content']}"
                    for r in results
                ])
                sources = ", ".join([r['url'] for r in results])
                logger.info(f"Tavily returned {len(results)} results")
            else:
                tavily_results = "No external results found."
        except Exception as e:
            logger.warning(f"Tavily search failed: {e}")
            tavily_results = "External search unavailable."
        timings["tavily"] = time.perf_counter() - t1
        logger.info(f"Timing — Tavily: {timings['tavily']:.2f}s")

        # Step 3 — Claude synthesis
        t2 = time.perf_counter()
        anthropic_client = anthropic.AsyncAnthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )

        today = date.today().strftime("%B %d, %Y")

        # Build the original user prompt (used either as the new request or
        # as the first turn in the refinement conversation history)
        user_prompt = USER_TEMPLATE.format(
            topic=topic,
            rts_results=rts_results,
            tavily_results=tavily_results,
            date=today,
            sources=sources
        )

        if existing_brief:
            refinement_prompt = REFINEMENT_TEMPLATE.format(
                refinement_request=refinement_request
            )
            messages = [
                {"role": "user", "content": user_prompt},
                {"role": "assistant", "content": existing_brief},
                {"role": "user", "content": refinement_prompt}
            ]
        else:
            messages = [
                {"role": "user", "content": user_prompt}
            ]

        response = await anthropic_client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=messages # type: ignore
        )

        brief = next(block.text for block in response.content if block.type == "text")
        timings["claude"] = time.perf_counter() - t2
        logger.info(f"Timing — Claude: {timings['claude']:.2f}s")
        logger.info(f"Timing — Total: {sum(timings.values()):.2f}s")

        return brief

    except Exception as e:
        logger.exception(f"Research failed: {e}")
        return f"*Brief: {topic}*\n\nFailed to generate research. Please try again."