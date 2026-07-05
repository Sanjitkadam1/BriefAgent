def build_app_home_view(
    install_url: str | None = None, is_connected: bool = False
) -> dict:
    blocks = [
        # Header
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "BriefAgent"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Executive research briefs, synthesized from your team's Slack context and live market data — in seconds."
            }
        },
        {"type": "divider"},

        # How to use
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*How to use*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*1.* Open BriefAgent from the sidebar\n*2.* Type any topic — a company, market, policy, or question\n*3.* Receive a structured brief in seconds\n*4.* Refine it through conversation\n*5.* Save as a Canvas and share with your team"
            }
        },
        {"type": "divider"},

        # Example topics
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Example topics*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "— `NVIDIA market position`\n— `Fed rate decision impact on fintech`\n— `Tesla vs GM EV strategy`\n— `Pfizer obesity drug pipeline`\n— `AI chip competitive landscape`"
            }
        },
        {"type": "divider"},

        # What BriefAgent pulls in
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*What BriefAgent pulls in*"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Internal context*\nRelevant messages and discussions from this workspace"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Live web data*\nCurrent market stats, news, and competitor information"
                }
            ]
        },
        {"type": "divider"},

        # Brief structure
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Every brief includes*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Executive Summary  ·  Market Overview  ·  Key Data Points\nCompetitive Landscape  ·  Risks  ·  Internal Context  ·  Recommendations"
            }
        },
        {"type": "divider"},

        # Footer context
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "BriefAgent uses Slack's Real-Time Search API, Tavily, and Claude AI to generate briefs."
                }
            ]
        }
    ]

    return {
        "type": "home",
        "blocks": blocks,
    }