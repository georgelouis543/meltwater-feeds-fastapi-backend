import logging
import os

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.controllers.auth.tokens_controller import create_access_token

load_dotenv()

ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
ALGORITHM = os.getenv("ALGORITHM")


async def handle_refresh_token(
        request: Request,
        user_collection
):
    # Retrieve the refresh token from cookie
    refresh_token = request.cookies.get('jwt')
    user_collection = user_collection

    if not refresh_token:
        raise HTTPException(401, detail="Unauthorized! Cookie missing!")

    logging.info(f"successfully retrieved Refresh Token: {refresh_token}")
    logging.info(f"All Request Headers: {request.headers}")

    # Fetch user from the database
    found_user = await user_collection.find_one({
        "refresh_token": refresh_token
    })

    if not found_user:
        raise HTTPException(401, detail="Unauthorized")

    # Decode the refresh token
    try:
        decoded_refresh_token = jwt.decode(
            refresh_token,
            REFRESH_TOKEN_SECRET,
            algorithms=ALGORITHM,
            verify=True
        )
        logging.info(f"SUCCESSFULLY DECODED REFRESH TOKEN: {decoded_refresh_token}")

    except Exception as e:
        logging.info(f'Exited with Exception: {e}')
        raise HTTPException(403, detail="Forbidden!")

    # Validate the token email with the user email
    if decoded_refresh_token["user_email"] == found_user["user_email"]:
        access_token = create_access_token(
            found_user["user_email"],
            found_user["user_name"],
            found_user["user_role"]
        )
        data_to_return = {
            "access_token": access_token,
            "token_type": "Bearer",
            "user_email": found_user["user_email"],
            "user_role": found_user["user_role"]
        }
        response = JSONResponse(content=data_to_return)
        return response

    else:
        raise HTTPException(403, detail="Forbidden!")