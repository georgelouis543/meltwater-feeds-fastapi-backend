from fastapi import APIRouter, Depends, Response

from app.controllers.html_to_rss.crud.create_feed_controller import create_feed
from app.controllers.html_to_rss.get_rss_controller import get_rss_feed
from app.controllers.html_to_rss.parser_controller import parse_input_html
from app.middleware.verify_jwt import verify_access_token
from app.middleware.verify_roles import verify_user_role
from app.models.documents_collection.document import get_documents_collection
from app.models.feeds_collection.feed import get_feed_collection
from app.models.html_to_rss.render_cache import get_render_cache_collection
from app.routers.auth_routes import oauth2_scheme
from app.schema.html_to_rss import HtmlRssFeedBase, HtmlRssFeedRequest, HtmlRssFeedResponse

router = APIRouter(
    prefix="/html-to-rss-convert",
    tags=["html-to-rss-convert"]
)

ALLOWED_ROLES = ["user", "admin"]


@router.get("")
async def root() -> dict:
    return {"message": "HTML to RSS converter Routes"}


@router.post("/get-preview")
async def get_preview(
        xpath_params: HtmlRssFeedBase,
        token: str = Depends(oauth2_scheme),
        render_cache_collection=Depends(get_render_cache_collection)
) -> list[dict]:
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    preview_items = await parse_input_html(
        xpath_params,
        render_cache_collection
    )
    return preview_items


@router.post("/save-feed", response_model=HtmlRssFeedResponse)
async def save_feed(
        feed_request: HtmlRssFeedRequest,
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
        render_cache_collection
    )
    return result_data


@router.get("/get-feed")
async def get_feed(
        feed_id: str,
        documents_collection=Depends(get_documents_collection),
        feed_collection=Depends(get_feed_collection),
        render_cache_collection=Depends(get_render_cache_collection)
):
    result = await get_rss_feed(
        feed_id,
        documents_collection,
        feed_collection,
        render_cache_collection
    )
    return Response(
        content=result,
        media_type="text/rss+xml"
    )