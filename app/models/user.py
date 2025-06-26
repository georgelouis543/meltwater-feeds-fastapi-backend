from fastapi import Request


async def get_user_collection(request: Request):
    return request.app.database["user_collection"]