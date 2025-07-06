from fastapi import APIRouter, Depends

from app.controllers.feed_collection_controllers.get_feeds_controller import get_feeds_handler
from app.middleware.verify_jwt import verify_access_token
from app.middleware.verify_roles import verify_user_role
from app.models.html_to_rss.feed import get_feed_collection
from app.routers.auth_routes import oauth2_scheme

router = APIRouter(
    prefix="/feed-collection-handler",
    tags=["feed-collection-handler"]
)

ALLOWED_ROLES = ["user", "admin"]

@router.get("")
async def root() -> dict:
    return {"message": "feed collection routes"}


@router.get("/get-all-feeds")
async def get_all_feeds(
        token: str = Depends(oauth2_scheme),
        feed_collection = Depends(get_feed_collection)
):
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    feeds = await get_feeds_handler(feed_collection)
    return feeds