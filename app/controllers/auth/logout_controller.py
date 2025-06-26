import logging

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def handle_logout(
        request: Request,
        user_collection
):
    # Get the refresh token from cookies
    refresh_token = request.cookies.get("jwt")

    if not refresh_token:
        raise HTTPException(204, detail="Could not authorize User!")

    # Fetch user from database
    found_user = await user_collection.find_one({
        "refresh_token": refresh_token
    })

    if not found_user:
        raise HTTPException(401, detail="Could not authorize User!")

    # The following try-catch is to handle DB Errors (if any)
    try:
        # Clear refresh token in database
        reset_token = {
            "$set": {
                "refresh_token": ""
            }
        }
        await user_collection.update_one(
            {
                "user_email": found_user["user_email"]
            }, reset_token
        )

        # Create response and delete cookie
        response = JSONResponse(
            content={
                "message": "Logout success!"
            },
            status_code=200
        )
        response.delete_cookie(
            key="jwt",
            httponly=True,
            samesite='none',
            secure=True
        )
        logging.info("LOGOUT SUCCESS")
        return response

    except HTTPException as e:
        logging.warning(f"Exited with Exception {e}")
        raise e

    except Exception as e:
        logging.warning(f"Exited with Exception {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")