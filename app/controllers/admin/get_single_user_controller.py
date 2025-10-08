import logging

from bson import ObjectId
from fastapi import HTTPException

from app.helpers.mongo_doc_serializer import individual_doc_serialize


async def get_single_user_handler(
        user_collection,
        user_id: str
):
    try:
        feed_cursor = await user_collection.find_one({
            "_id": ObjectId(user_id)
        })

        if not feed_cursor:
            raise HTTPException(status_code=404, detail="User not found!")

        user_data = individual_doc_serialize(feed_cursor)

        return user_data

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.warning(f"Exception {e} occurred while fetching User data for UserID: {user_id}")
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong when fetching User Data for UserID: {user_id}"
        )