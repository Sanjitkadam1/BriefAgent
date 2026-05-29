async def brief_command(ack, respond, command):
    await ack()
    topic = command.get("text", "").strip()
    if not topic:
        await respond("Please provide a topic. Usage: `/brief [topic]`")
        return
    await respond(f"Got it! Researching: *{topic}*... (full brief coming soon)")