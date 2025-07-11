from fastapi import APIRouter, Depends

from app.controllers.rss_playground.parser_controller import parse_input_rss
from app.middleware.verify_jwt import verify_access_token
from app.middleware.verify_roles import verify_user_role
from app.models.render_cache import get_render_cache_collection
from app.routers.auth_routes import oauth2_scheme
from app.schema.rss_playground import RssToMWFeedBase

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