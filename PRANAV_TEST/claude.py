import anthropic 
from dotenv import load_dotenv



load_dotenv()
async def generate_brief(user_query, tavily_results):    
    if (user_query != "" and tavily_results != ""): 
        client = anthropic.AsyncAnthropic()

        message = await client.messages.create(
            system = "You are a part of the architecture of a Slack command called BreifBot. Provide the user a usful summary of the information provided based on their specifications and needs. If sources provided aren't reliable or specific enough to user's specifications or don't match them ONLY then do additional reaserach and summarize it in the appropriate manner.", 
            model = "claude-sonnet-4-6", 
            max_tokens = 1000,
            messages = [ {
                "role": "user", 
                "content": user_query + " tavily findings: " + str(tavily_results)
                }
            ], 
        )
        print(message.content[0].text)
        return (message.content[0].text)
