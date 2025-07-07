from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.controllers.feed_collection_controllers.get_feed_params_controller import get_individual_feed_params
from app.controllers.feed_collection_controllers.get_feeds_controller import get_feeds_handler
from app.middleware.verify_jwt import verify_access_token
from app.middleware.verify_roles import verify_user_role
from app.models.feed_collection_model import get_feed_collection
from app.routers.auth_routes import oauth2_scheme
from app.schema.feed_collection_schema import FeedsCollectionResponse

router = APIRouter(
    prefix="/feed-collection-handler",
    tags=["feed-collection-handler"]
)

ALLOWED_ROLES = ["user", "admin"]

@router.get("")
async def root() -> dict:
    return {"message": "feed collection routes"}


@router.get(
    "/get-all-feeds",
    response_model=FeedsCollectionResponse
)
async def get_all_feeds(
        token: str = Depends(oauth2_scheme),
        page: int = Query(1, ge=1),
        size: int = Query(15, ge=1, le=15),
        feed_id: Optional[str] = None, # Just _id
        created_by: Optional[str] = None,
        feed_collection = Depends(get_feed_collection)
):
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    feeds = await get_feeds_handler(
        feed_collection,
        page,
        size,
        feed_id,
        created_by
    )
    return feeds


@router.get("/get-single-feed-params")
async def get_single_feed(
        feed_id: str,
        token: str = Depends(oauth2_scheme),
        feed_collection = Depends(get_feed_collection)
):
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    feed = await get_individual_feed_params(
        feed_collection,
        feed_id
    )
    return feed