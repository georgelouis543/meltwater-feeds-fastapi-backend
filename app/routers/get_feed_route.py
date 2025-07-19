from fastapi import (
    APIRouter,
    Query,
    Depends
)
from starlette.responses import Response

from app.controllers.getfeed_controllers.get_rss_controller import get_rss_feed
from app.middleware.verify_feed_id import verify_original_feed_id
from app.models.document import get_documents_collection
from app.models.feed_collection_model import get_feed_collection

router = APIRouter(
    prefix="/getfeed",
    tags=["get-feed"]
)

@router.get("/")
async def get_rss_feed_response(
    feed_id: str = Query(default=None), # for new version
    id_: str = Query(default=None, alias="id"), # for legacy version
    documents_collection=Depends(get_documents_collection),
    feed_collection=Depends(get_feed_collection)
):
    original_id = verify_original_feed_id(id_, feed_id)
    result = await get_rss_feed(
        original_id,
        documents_collection,
        feed_collection
    )
    return Response(
        content=result,
        media_type="text/rss+xml"
    )