from fastapi import (
    APIRouter,
    Query,
    HTTPException
)

router = APIRouter(
    prefix="/getfeed",
    tags=["get-feed"]
)

@router.get("/")
async def get_rss_feed(
    feed_id: str = Query(default=None), # for new version
    id_: str = Query(default=None, alias="id") # for legacy version
):
    original_id = feed_id or id_
    if not original_id:
        raise HTTPException(status_code=400, detail="Missing feed_id or id parameter")

    return original_id