import datetime

from bson import ObjectId
from fastapi import HTTPException

from app.schema.merge_feeds import MergeFeed


async def merge_feeds_handler(
        feed_metadata: MergeFeed,
        feed_collection,
        auth_token
):
    try:
        feed_metadata = dict(feed_metadata)

        ids_to_merge = set(feed_metadata["feed_ids"])
        if len(ids_to_merge) < 2 or len(ids_to_merge) > 5:
            raise HTTPException(
                status_code=400,
                detail="Nothing to merge or too much to merge!"
            )


        for feed_id in ids_to_merge:
            found_feed_cursor = await feed_collection.find_one({
                "_id": ObjectId(feed_id)
            })

            if not found_feed_cursor:
                raise HTTPException(
                    status_code=400,
                    detail="One of the entered feed_ids is not valid. Please check again!"
                )

            if (
                    found_feed_cursor["feed_type"] == "legacy_feed" or
                    found_feed_cursor["feed_type"] == "merged_feed"
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"The feed with id {feed_id} is not available to be merged due to its type. "
                           "Please check again!"
                )


        feed_metadata["created_by"] = auth_token["user_email"]
        feed_metadata["created_at"] = datetime.datetime.now(datetime.UTC)
        feed_metadata["updated_at"] = datetime.datetime.now(datetime.UTC)

        saved_merged_feed = await feed_collection.insert_one(feed_metadata)
        saved_feed_id = saved_merged_feed.inserted_id

        return {
            "message": f"Feeds have been Merged Successfully! Feed ID: {str(saved_feed_id)}",
            "success": True
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while merging feeds! Please try again later."
        )
