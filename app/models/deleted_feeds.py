from fastapi import Request


async def get_deleted_feeds_collection(
        request: Request
):
    return request.app.database["deleted_feeds_collection"]