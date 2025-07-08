import datetime
import logging

from bson import ObjectId
from fastapi import HTTPException


async def duplicate_feed_handler(
        feed_id: str,
        feed_collection,
        auth_token
):
    try:
        original_feed_cursor = await feed_collection.find_one({
            "_id": ObjectId(feed_id)
        }, {"_id": 0})

        if not original_feed_cursor:
            raise HTTPException(status_code=404, detail="Feed not found")

        original_feed_cursor["created_by"] = auth_token["user_email"]
        original_feed_cursor["created_at"] = datetime.datetime.now(datetime.UTC)
        original_feed_cursor["updated_at"] = datetime.datetime.now(datetime.UTC)

        duplicated_feed = await feed_collection.insert_one(original_feed_cursor)
        duplicated_feed_id = duplicated_feed.inserted_id

        return {
            "message": f"Feed has been Duplicated Successfully! Feed ID: {str(duplicated_feed_id)}",
            "success": True
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.warning(f"An Exception: {e} occurred when duplicating the feed with ID: {feed_id}")
        raise HTTPException(status_code=500, detail="Could not duplicate feed!")