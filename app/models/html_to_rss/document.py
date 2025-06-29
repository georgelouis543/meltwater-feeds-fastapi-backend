from fastapi import Request


async def get_documents_collection(request: Request):
    return request.app.database["documents_collection"]