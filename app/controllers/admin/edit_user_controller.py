import logging

from bson import ObjectId
from fastapi import HTTPException
from starlette.responses import Response

from app.schema.user import UserUpdate


async def update_user_handler(
        user_id: str,
        update_info: UserUpdate,
        user_collection
):
    try:
        update_info = dict(update_info)
        get_user = await user_collection.find_one({
            "_id": ObjectId(user_id)
        })

        if not get_user:
            raise HTTPException(status_code=404, detail="User not found!")

        final_data_to_update = {}
        field_changed = False

        if get_user["user_email"] != update_info["user_email"]:
            is_duplicate = await user_collection.find_one({
                "user_email": update_info["user_email"]
            })
            if is_duplicate:
                raise HTTPException(status_code=409, detail="Email already exists!")

            final_data_to_update["user_email"] = update_info["user_email"]
            field_changed = True

        if get_user["user_name"] != update_info["user_name"]:
            is_duplicate = await user_collection.find_one({
                "user_name": update_info["user_name"]
            })
            if is_duplicate:
                raise HTTPException(status_code=409, detail="Username already exists!")

            final_data_to_update["user_name"] = update_info["user_name"]
            field_changed = True

        if get_user["user_role"] != update_info["user_role"]:
            final_data_to_update["user_role"] = update_info["user_role"]
            field_changed = True

        if not field_changed:
            return Response(status_code=204)

        final_data_to_update["created_at"] = get_user["created_at"]
        final_data_to_update["updated_at"] = update_info["updated_at"]

        await user_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": final_data_to_update}
        )

        return {
                "user_id": user_id,
                "message": f"User updated successfully with id: {user_id}",
                "success": True
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.warning(f"An Exception {e} occurred while editing user.")
        raise HTTPException(
            status_code=500,
            detail=f"Exception {e} occurred while editing the user. Try again later."
        )