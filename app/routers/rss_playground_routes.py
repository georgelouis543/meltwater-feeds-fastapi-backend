from fastapi import APIRouter, Depends

from app.controllers.rss_playground.crud.create_feed_controller import create_feed
from app.controllers.rss_playground.parser_controller import parse_input_rss
from app.middleware.verify_jwt import verify_access_token
from app.middleware.verify_roles import verify_user_role
from app.models.document import get_documents_collection
from app.models.feed_collection_model import get_feed_collection
from app.models.render_cache import get_render_cache_collection
from app.routers.auth_routes import oauth2_scheme
from app.schema.rss_playground import (
    RssToMWFeedBase,
    RssToMWFeedResponse,
    RssToMWFeedRequest
)

router = APIRouter(
    prefix="/rss-playground",
    tags=["rss-playground"]
)

ALLOWED_ROLES = ["user", "admin"]


@router.get("")
async def root() -> dict:
    return {"message": "RSS Playground Routes"}


@router.post("/get-preview")
async def get_preview(
        xpath_params: RssToMWFeedBase,
        token: str = Depends(oauth2_scheme),
        render_cache_collection=Depends(get_render_cache_collection)
) -> list[dict]:
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    preview_items = await parse_input_rss(
        xpath_params,
        render_cache_collection
    )
    return preview_items


@router.post(
    "/save-feed",
    response_model=RssToMWFeedResponse
)
async def save_feed(
        feed_request: RssToMWFeedRequest,
        token: str = Depends(oauth2_scheme),
        feed_collection=Depends(get_feed_collection),
        documents_collection=Depends(get_documents_collection),
        render_cache_collection=Depends(get_render_cache_collection)
):
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    result_data = await create_feed(
        feed_request,
        feed_collection,
        documents_collection,
        render_cache_collection,
        decoded_access_token
    )
    return result_data