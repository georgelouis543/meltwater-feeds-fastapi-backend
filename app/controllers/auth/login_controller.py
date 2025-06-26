import logging

from fastapi import HTTPException
from starlette.responses import JSONResponse

from app.controllers.auth.tokens_controller import create_refresh_token, create_access_token


async def handle_login(user_email: str, user_collection):
    try:
        # Fetch user from the database using find_one
        user_collection = user_collection
        found_user = await user_collection.find_one({
            "user_email": user_email
        })

        if not found_user:
            raise HTTPException(status_code=401, detail="Unauthorized!")

        # Generate tokens
        refresh_token = create_refresh_token(
            found_user["user_email"],
            found_user["user_name"],
            found_user["user_role"]
        )

        access_token = create_access_token(
            found_user["user_email"],
            found_user["user_name"],
            found_user["user_role"]
        )

        # Update refresh token in the database
        update_data = {
            "$set": {
                "refresh_token": refresh_token
            }
        }
        await user_collection.update_one(
            {
                "user_email": user_email
            }, update_data
        )

        # Prepare response data
        data_to_return = {
            "access_token": access_token,
            "token_type": "Bearer",
            "user_email": found_user["user_email"],
            "user_role": found_user["user_role"]
        }

        # Set JWT token as HTTP-only cookie
        response = JSONResponse(content=data_to_return)
        response.set_cookie(
            key="jwt",
            value=refresh_token,
            expires=3600,
            httponly=True,
            samesite="none",
            secure=True
        )

        return response

    except HTTPException as e:
        logging.warning(f"Exited with Exception {e}")
        raise e

    except Exception as e:
        logging.warning(f"Exited with Exception {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error!")
