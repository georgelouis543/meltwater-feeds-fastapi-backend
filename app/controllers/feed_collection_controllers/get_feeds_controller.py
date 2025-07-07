import logging
from math import ceil

from bson import ObjectId
from pymongo import DESCENDING

from app.helpers.mongo_doc_serializer import list_mongo_collection_serialize


async def get_feeds_handler(
        feed_collection,
        page: int,
        size: int,
        feed_id: str,
        created_by: str
) -> dict:
    try:
        query_filter = {}

        # Sort by latest feeds if no query is passed (and by default)
        sort_order = [("updated_at", DESCENDING)]

        skip = (page - 1) * size

        if feed_id:
            query_filter["_id"] = ObjectId(feed_id)

        if created_by:
            query_filter["created_by"] = created_by

        feeds_cursor = feed_collection.find(
            query_filter
        ).sort(sort_order).skip(skip).limit(size)

        feeds_raw = await feeds_cursor.to_list(length=None)

        total = await feed_collection.count_documents(
            query_filter
        )

        pages = ceil(total / size)

        feeds_to_return = list_mongo_collection_serialize(feeds_raw)

        return {
            "feeds": feeds_to_return,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages
        }

    except Exception as e:
        logging.warning(f"Exception while retrieving all feeds: {e}")
        return {
            "feeds": [],
            "total": 0,
            "page": 0,
            "size": 0,
            "pages": 0
        }

