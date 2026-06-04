import anthropic 
from dotenv import load_dotenv

# This import is simply meant for testing, delete it during real development.
import asyncio 

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

# This is just for testing, delete this during actual development of code.
asyncio.run(generate_brief("What are the latest details on the SpaceX IPO valuation and ticker symbol?", [{'title': 'SpaceX (SPCX) IPO: Live updates - CNBC', 'url': 'https://cnbc.com', 'content': 'Elon Musk’s SpaceX is officially headed for the public market in what’s likely to be a record IPOthat will put the world’s richest person at the helm of two separate trillion-dollar publicly traded companies.\n\nIn a prospectus with the Securities and Exchange Commission on Wednesday, SpaceX said it plans to list under ticker symbol SPCX on the Nasdaq. SpaceX confidentially filed with the SEC in April, and CNBC reported last week that the company is aiming to kick off a roadshow to market the dea'}, {'title': 'SpaceX Said to Target $75 Billion in IPO at $135Per Share', 'url': 'https://youtube.com', 'content': 'actually came out of Rocket Lab sort of came out of the rocket business, which is a little bit surprising to me, but I still think sort of the, the, you know, the long term play here is the data center in space and I so but we had we had a combined again analysis in all those industries to really, uh, come up with what we thought maybe a plausible valuation albeit extremely lofty valuation would be. Is there an expectation, George, that, um, Elon may look to just kind of consolidate all of his h'}, {'title': 'Your SpaceX IPO Questions, Answered - YouTube', 'url': 'https://youtube.com', 'content': "like, uh, asteroid mining, um, the mass driver. Uh, you know, the logistics in terms of exactly how this would work, I I think are yet to be seen. Um, but, uh, again, we've seen, um, Elon accomplish what what previously sounded sounded crazy. Um, so, uh, you know, whether or not you think these are are crazy ideas, um, it seems like maybe thisis the company to do it. Yeah, exactly. And maybe just one other business line to mention is point-to-point travel with Starship. So going from uh one pla"}, {'title': 'Elon Musk could become trillionaire as SpaceX eyes IPO - YouTube', 'url': 'https://youtube.com', 'content': 'Dan Ives, financial analyst and senior equity analyst at Wedbush Securities, discusses a potential SpaceX IPO and what it could mean for Musk and investors. Subscribe to ABC News on YouTube: ABC News is your daily source of breaking national and world news, exclusive interviews and 24/7 live streaming coverage. Download the ABC News app for the latest headlines and alerts: Watch 24/7 coverage of breaking news and live events on ABC News Live: Image 11•LIVE:Latest News Headlines and Events l A.'}]))