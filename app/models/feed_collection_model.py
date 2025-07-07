from fastapi import Request


async def get_feed_collection(request: Request):
    return request.app.database["feed_collection"]