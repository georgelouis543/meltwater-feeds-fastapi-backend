from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.controllers.admin.create_user_controller import create_user_handler
from app.controllers.admin.delete_user_controller import delete_user_handler
from app.controllers.admin.edit_user_controller import update_user_handler
from app.controllers.admin.get_single_user_controller import get_single_user_handler
from app.controllers.admin.view_users_controller import get_users_handler
from app.middleware.verify_jwt import verify_access_token
from app.middleware.verify_roles import verify_user_role
from app.models.user import get_user_collection
from app.routers.auth_routes import oauth2_scheme
from app.schema.user import UserCreate, UserUpdate, UsersCollectionResponse, DeleteUserResponse

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


@router.get("/get-user/{user_id}")
async def get_single_user(
        user_id: str,
        token: str = Depends(oauth2_scheme),
        user_collection = Depends(get_user_collection)
):
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    result = await get_single_user_handler(
        user_collection,
        user_id
    )
    return result


# Get Paginated Users
@router.get(
    "/get-all-users",
    response_model = UsersCollectionResponse
)
async def get_all_users(
        token: str = Depends(oauth2_scheme),
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=10),
        user_id: Optional[str] = None,  # Just _id
        user_email: Optional[str] = None,
        user_name: Optional[str] = None,
        user_collection = Depends(get_user_collection)
):
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    users_list = await get_users_handler(
        user_collection,
        page,
        size,
        user_id,
        user_email,
        user_name
    )
    return users_list


@router.delete(
    "/delete-user/{user_id}",
    response_model=DeleteUserResponse
)
async def delete_single_user(
        user_id: str,
        token: str = Depends(oauth2_scheme),
        user_collection=Depends(get_user_collection),
):
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    delete_user_result = await delete_user_handler(
        user_collection,
        user_id
    )
    return delete_user_result


