from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.controllers.auth.login_controller import handle_login
from app.controllers.auth.logout_controller import handle_logout
from app.controllers.auth.refresh_controller import handle_refresh_token
from app.middleware.verify_gjwt import verify_google_token
from app.models.user import get_user_collection
from app.schema.token import TokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("")
async def root() -> dict:
    return {"message": "Auth Routes"}


@router.get("/login", response_model=TokenResponse)
async def login(
        google_token_verification_result: dict = Depends(verify_google_token),
        user_collection = Depends(get_user_collection)
):
    response = await handle_login(
        google_token_verification_result["email"],
        user_collection
    )
    return response


@router.get("/refresh", response_model=TokenResponse)
async def refresh(
        request: Request,
        user_collection = Depends(get_user_collection)
):
    response = await handle_refresh_token(request, user_collection)
    return response


@router.get("/logout")
async def logout(
        request: Request,
        user_collection = Depends(get_user_collection)
):
    response = await handle_logout(request, user_collection)
    return response