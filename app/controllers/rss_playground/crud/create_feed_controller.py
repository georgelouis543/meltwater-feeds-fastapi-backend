import logging
import os

from dotenv import load_dotenv
from fastapi import HTTPException

from app.controllers.rss_playground.crud.save_items_controller import save_items
from app.controllers.rss_playground.parser_controller import parse_input_rss
from app.schema.rss_playground import RssToMWFeedRequest

load_dotenv()
GET_FEED_ENDPOINT = os.getenv("GET_FEED_ENDPOINT")


async def create_feed(
        feed_request: RssToMWFeedRequest,
        feed_collection,
        documents_collection,
        render_cache_collection,
        auth_token
) -> dict:
    try:
        feed_request = feed_request
        #securely adding the author of the feed
        feed_request.created_by = auth_token["user_email"]

        save_feed = await feed_collection.insert_one(dict(feed_request))
        saved_feed_id = str(save_feed.inserted_id)

        get_items = await parse_input_rss(
            feed_request,
            render_cache_collection
        )

        await save_items(
            saved_feed_id,
            get_items,
            documents_collection
        )

        data_to_return = {
            "feed_id": saved_feed_id,
            "feed_url":f"{GET_FEED_ENDPOINT}{saved_feed_id}",
            "success": True
        }

        return data_to_return

    except Exception as e:
        logging.warning(f"An Exception {e} occurred while creating your feed")
        raise HTTPException(
            status_code=500,
            detail=f"Exception {e} occurred while creating your feed. Try again later."
        )