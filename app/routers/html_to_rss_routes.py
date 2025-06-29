from fastapi import APIRouter, Depends

from app.controllers.html_to_rss.crud.create_feed_controller import create_feed
from app.controllers.html_to_rss.parser_controller import parse_input_html
from app.models.html_to_rss.document import get_documents_collection
from app.models.html_to_rss.feed import get_feed_collection
from app.models.html_to_rss.render_cache import get_render_cache_collection
from app.schema.html_to_rss import HtmlRssFeedBase, HtmlRssFeedRequest, HtmlRssFeedResponse

router = APIRouter(
    prefix="/html-to-rss-convert",
    tags=["html-to-rss-convert"]
)


@router.get("/")
async def root() -> dict:
    return {"message": "HTML to RSS converter Routes"}


@router.post("/get-preview")
async def get_preview(
        xpath_params: HtmlRssFeedBase,
        render_cache_collection=Depends(get_render_cache_collection)
):
    preview_items = await parse_input_html(xpath_params, render_cache_collection)
    return preview_items

@router.post("/save-feed", response_model=HtmlRssFeedResponse)
async def save_feed(
        feed_request: HtmlRssFeedRequest,
        feed_collection=Depends(get_feed_collection),
        documents_collection=Depends(get_documents_collection),
        render_cache_collection=Depends(get_render_cache_collection)
):
    result_data = await create_feed(
        feed_request,
        feed_collection,
        documents_collection,
        render_cache_collection
    )
    return result_data
