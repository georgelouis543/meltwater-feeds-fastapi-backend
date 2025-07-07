from fastapi import Request


async def get_render_cache_collection(request: Request):
    return request.app.database["render_cache"]