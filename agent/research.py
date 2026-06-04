import os
import anthropic
from search import search_tavily

async def run_research(topic, action_token, client, logger, existing_brief=None):
    try:
        # Step 1 — RTS API: pull internal Slack context
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
                messages = rts_response.get("messages", [])
                if messages:
                    rts_results = "\n".join([
                        f"- {m.get('text', '')}" for m in messages[:10]
                    ])
                    logger.info(f"RTS returned {len(messages)} messages")
                else:
                    rts_results = "No relevant internal messages found."
            except Exception as e:
                logger.warning(f"RTS API call failed: {e}")
                rts_results = "Internal search unavailable."

        # Step 2 — Tavily: pull external web data
        tavily_results = ""
        try:
            results = await search_tavily(topic)
            if results:
                tavily_results = "\n".join([
                    f"- *{r['title']}* ({r['url']})\n  {r['content']}"
                    for r in results
                ])
                logger.info(f"Tavily returned {len(results)} results")
            else:
                tavily_results = "No external results found."
        except Exception as e:
            logger.warning(f"Tavily search failed: {e}")
            tavily_results = "External search unavailable."

        # Step 3 — Claude synthesis
        anthropic_client = anthropic.AsyncAnthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )

        if existing_brief:
            prompt = f"""You are BriefAgent, a research assistant inside Slack.

The user has requested a refinement to their existing brief.

EXISTING BRIEF:
{existing_brief}

USER REFINEMENT REQUEST:
{topic}

INTERNAL SLACK CONTEXT:
{rts_results}

EXTERNAL WEB DATA:
{tavily_results}

Please update the brief based on the user's request. Keep the same structure but apply their changes.
Return only the updated brief, formatted in Slack mrkdwn."""

        else:
            prompt = f"""You are BriefAgent, a research assistant inside Slack.

Generate a structured research brief on the following topic for a business team.

TOPIC: {topic}

INTERNAL SLACK CONTEXT (what the team has already discussed):
{rts_results}

EXTERNAL WEB DATA (live search results):
{tavily_results}

Format the brief in Slack mrkdwn with these sections:
*📊 Overview*
*🔍 Key Findings*
*⚠️ Risks & Challenges*
*🎯 Recommendations*

Keep it concise and actionable. Use bullet points."""

        response = await anthropic_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        brief = response.content[0].text
        return brief

    except Exception as e:
        logger.exception(f"Research failed: {e}")
        return f"*Brief: {topic}*\n\nFailed to generate research. Please try again."