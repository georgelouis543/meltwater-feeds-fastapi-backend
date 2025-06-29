import logging
import os

from dotenv import load_dotenv
from fastapi import HTTPException

from app.controllers.html_to_rss.crud.save_items_controller import save_items
from app.controllers.html_to_rss.parser_controller import parse_input_html
from app.schema.html_to_rss import HtmlRssFeedRequest

load_dotenv()
GET_FEED_ENDPOINT = os.getenv("GET_FEED_ENDPOINT")

async def create_feed(
        feed_request: HtmlRssFeedRequest,
        feed_collection,
        documents_collection,
        render_cache_collection
) -> dict:
    try:
        feed_request = feed_request

        save_feed = await feed_collection.insert_one(dict(feed_request))
        saved_feed_id = str(save_feed.inserted_id)

        get_items = await parse_input_html(
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