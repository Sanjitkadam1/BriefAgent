async def upload_brief_as_file(client, channel_id, topic, brief, logger):
    """Upload a raw markdown brief file into the Slack conversation."""
    try:
        response = await client.files_upload_v2(
            channel=channel_id,
            content=brief,
            filename=f"Brief - {topic}.md",
            title=f"Brief: {topic}",
        )
        logger.info(f"Brief uploaded as file to {channel_id}")
        return response.get("file", {}).get("permalink")
    except Exception as e:
        logger.exception(f"File upload failed: {e}")
        return None