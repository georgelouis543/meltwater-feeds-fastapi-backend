import logging
from math import ceil

from bson import ObjectId
from fastapi import HTTPException
from pymongo import DESCENDING

from app.helpers.mongo_doc_serializer import list_mongo_collection_serialize


async def get_users_handler(
        user_collection,
        page: int,
        size: int,
        user_id: str,
        user_email: str,
        user_name: str
) -> dict:
    try:
        query_filter = {}

        # Sort by latest feeds if no query is passed (and by default)
        sort_order = [("updated_at", DESCENDING)]

        skip = (page - 1) * size

        if user_id:
            query_filter["_id"] = ObjectId(user_id)

        if user_email:
            query_filter["user_email"] = user_email

        if user_name:
            query_filter["user_name"] = user_name

        feeds_cursor = user_collection.find(
            query_filter
        ).sort(sort_order).skip(skip).limit(size)

        users_raw = await feeds_cursor.to_list(length=None)

        total = await user_collection.count_documents(
            query_filter
        )

        pages = ceil(total / size)

        users_to_return = list_mongo_collection_serialize(users_raw)

        return {
            "users": users_to_return,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages
        }

    except Exception as e:
        logging.warning(f"Exception while retrieving all users: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong while retrieving all users: {e}"
        )
