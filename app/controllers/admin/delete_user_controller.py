import logging

from bson import ObjectId
from fastapi import HTTPException


async def delete_user_handler(
        user_collection,
        user_id: str
) -> dict:
    try:
        user_to_delete_cursor = await user_collection.find_one({
            "_id": ObjectId(user_id)
        })

        if not user_to_delete_cursor:
            raise HTTPException(
                status_code=404,
                detail=f"User with ID: {user_id} not found"
            )

        await user_collection.delete_one({
            "_id": ObjectId(user_id)
        })

        return {
            "message": f"User with id {user_id} has been successfully deleted!",
            "success": True
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.warning(f"There was an issue deleting User with ID: {user_id}. Exited with Exception {e}")
        raise HTTPException(
            status_code=500,
            detail=f"There was an issue deleting User with ID: {user_id}. Please try again later."
        )
