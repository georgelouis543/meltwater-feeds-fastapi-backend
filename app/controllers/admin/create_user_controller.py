import logging

from fastapi import HTTPException

from app.schema.user import UserBase


async def create_user_handler(
        new_user_info: UserBase,
        user_collection
) -> dict:
    try:
        new_user = dict(new_user_info)

        is_existing_user = await user_collection.find_one({
            "user_email": new_user["user_email"]
        })
        if is_existing_user:
            raise HTTPException(
                status_code=409,
                detail="User already exists!"
            )

        # Set an empty refresh token
        new_user["refresh_token"] = ""

        save_user = await user_collection.insert_one(new_user)
        saved_user_id = str(save_user.inserted_id)

        return {
            "user_id": saved_user_id,
            "message": f"User created successfully with id: {saved_user_id}",
            "success": True
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.warning(f"An Exception {e} occurred while creating user.")
        raise HTTPException(
            status_code=500,
            detail=f"Exception {e} occurred while creating the user. Try again later."
        )