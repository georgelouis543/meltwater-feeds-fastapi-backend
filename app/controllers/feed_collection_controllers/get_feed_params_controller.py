import logging

from bson import ObjectId
from fastapi import HTTPException

from app.helpers.mongo_doc_serializer import individual_doc_serialize


async def get_individual_feed_params(
        feed_collection,
        feed_id: str
):
    try:
        feed_cursor = await feed_collection.find_one({
            "_id": ObjectId(feed_id)
        })

        feed_data_to_return = individual_doc_serialize(feed_cursor)

        return feed_data_to_return

    except Exception as e:
        logging.warning(f"Exception {e} occurred while fetching your feed params for feedID: {feed_id}")
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong when fetching feed params for feed ID: {feed_id}"
        )

