from fastapi import APIRouter, Depends

from app.controllers.html_to_rss.fetcher_controller import get_static_html_page, get_javascript_page
from app.controllers.html_to_rss.parser_controller import parse_input_html
from app.models.html_to_rss.render_cache import get_render_cache_collection
from app.schema.html_to_rss import HtmlRssFeedBase

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
