from fastapi import APIRouter, Depends

from app.controllers.admin.create_user_controller import create_user_handler
from app.controllers.admin.edit_user_controller import update_user_handler
from app.middleware.verify_jwt import verify_access_token
from app.middleware.verify_roles import verify_user_role
from app.models.user import get_user_collection
from app.routers.auth_routes import oauth2_scheme
from app.schema.user import UserCreate, UserUpdate

router = APIRouter(
    prefix="/admin",
    tags=["admin-routes-handler"]
)

ALLOWED_ROLES = ["admin"]

@router.get("")
async def root() -> dict:
    return {"message": "Admin Routes"}


@router.post("/create-user")
async def create_new_user(
        user_info: UserCreate,
        token: str = Depends(oauth2_scheme),
        user_collection = Depends(get_user_collection)
) -> dict:
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    result = await create_user_handler(
        user_info,
        user_collection
    )
    return result


@router.put("/update-user/{user_id}")
async def update_user(
        user_id: str,
        user_info: UserUpdate,
        token: str = Depends(oauth2_scheme),
        user_collection = Depends(get_user_collection)
) -> dict:
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    result = await update_user_handler(
        user_id,
        user_info,
        user_collection
    )
    return result


