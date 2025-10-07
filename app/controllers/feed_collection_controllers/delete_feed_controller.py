import datetime
import logging

from bson import ObjectId
from fastapi import HTTPException


async def delete_feed_handler(
        auth_token,
        feed_collection,
        deleted_feeds_collection,
        feed_id: str
) -> dict:
    try:
        feed_to_delete_cursor = await feed_collection.find_one({
            "_id": ObjectId(feed_id)
        })

        if not feed_to_delete_cursor:
            raise HTTPException(
                status_code=404,
                detail=f"Feed with ID: {feed_id} not found"
            )

        delete_requested_by = auth_token["user_email"]
        feed_created_by = feed_to_delete_cursor["created_by"]

        if feed_created_by != delete_requested_by:
            raise HTTPException(
                status_code=403,
                detail="User not allowed to delete!"
            )

        # Adding the deleted_at timestamp (TTL would be 1 month)
        feed_to_delete_cursor["deleted_at"] = datetime.datetime.now(datetime.UTC)

        await deleted_feeds_collection.insert_one(
            feed_to_delete_cursor
        )
        logging.info(f"Feed with id: {feed_id} has been soft-deleted!")

        await feed_collection.delete_one({
            "_id": ObjectId(feed_id)
        })

        return {
            "message": f"Feed with id {feed_id} has been successfully deleted!",
            "success": True
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.warning(f"There was an issue deleting feed with ID: {feed_id}. Exited with Exception {e}")
        raise HTTPException(
            status_code=500,
            detail=f"There was an issue deleting feed with ID: {feed_id}. Please try again later."
        )
