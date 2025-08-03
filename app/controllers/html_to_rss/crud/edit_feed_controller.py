import os

from bson import ObjectId
from dotenv import load_dotenv
from fastapi import HTTPException

from app.schema.html_to_rss import HtmlRssFeedRequest

load_dotenv()
GET_FEED_ENDPOINT = os.getenv("GET_FEED_ENDPOINT")


async def update_html_to_rss_converted_feed(
        feed_id: str,
        feed_update_request: HtmlRssFeedRequest,
        access_token,
        feed_collection
):
    try:
        existing_feed_data = await feed_collection.find_one({
            "_id": ObjectId(feed_id)
        }, {"_id": 0})

        if not existing_feed_data:
            raise HTTPException(status_code=404, detail="Feed Not found!")

        new_feed_data = feed_update_request.model_dump()

        data_to_update = {}

        if existing_feed_data["url"] != new_feed_data["url"]:
            data_to_update["url"] = new_feed_data["url"]

        if existing_feed_data["is_javascript_enabled"] != new_feed_data["is_javascript_enabled"]:
            data_to_update["is_javascript_enabled"] = new_feed_data["is_javascript_enabled"]

        if existing_feed_data["feed_type"] != new_feed_data["feed_type"]:
            data_to_update["feed_type"] = new_feed_data["feed_type"]

        if existing_feed_data["item_xpath"] != new_feed_data["item_xpath"]:
            data_to_update["item_xpath"] = new_feed_data["item_xpath"]

        if existing_feed_data["title_xpath"] != new_feed_data["title_xpath"]:
            data_to_update["title_xpath"] = new_feed_data["title_xpath"]

        if existing_feed_data["description_xpath"] != new_feed_data["description_xpath"]:
            data_to_update["description_xpath"] = new_feed_data["description_xpath"]

        if existing_feed_data["date_regex"] != new_feed_data["date_regex"]:
            data_to_update["date_regex"] = new_feed_data["date_regex"]

        if existing_feed_data["date_xpath"] != new_feed_data["date_xpath"]:
            data_to_update["date_xpath"] = new_feed_data["date_xpath"]

        if existing_feed_data["use_index_date"] != new_feed_data["use_index_date"]:
            data_to_update["use_index_date"] = new_feed_data["use_index_date"]

        if existing_feed_data["item_url_pre_literal"] != new_feed_data["item_url_pre_literal"]:
            data_to_update["item_url_pre_literal"] = new_feed_data["item_url_pre_literal"]

        if existing_feed_data["item_url_xpath"] != new_feed_data["item_url_xpath"]:
            data_to_update["item_url_xpath"] = new_feed_data["item_url_xpath"]

        if existing_feed_data["item_url_post_literal"] != new_feed_data["item_url_post_literal"]:
            data_to_update["item_url_post_literal"] = new_feed_data["item_url_post_literal"]

        if existing_feed_data["source_name"] != new_feed_data["source_name"]:
            data_to_update["source_name"] = new_feed_data["source_name"]

        if existing_feed_data["source_url"] != new_feed_data["source_url"]:
            data_to_update["source_url"] = new_feed_data["source_url"]

        if existing_feed_data["image_url_pre_literal"] != new_feed_data["image_url_pre_literal"]:
            data_to_update["image_url_pre_literal"] = new_feed_data["image_url_pre_literal"]

        if existing_feed_data["image_url_xpath"] != new_feed_data["image_url_xpath"]:
            data_to_update["image_url_xpath"] = new_feed_data["image_url_xpath"]

        if existing_feed_data["image_url_post_literal"] != new_feed_data["image_url_post_literal"]:
            data_to_update["image_url_post_literal"] = new_feed_data["image_url_post_literal"]

        if existing_feed_data["default_image_url"] != new_feed_data["default_image_url"]:
            data_to_update["default_image_url"] = new_feed_data["default_image_url"]

        if existing_feed_data["feed_name"] != new_feed_data["feed_name"]:
            data_to_update["feed_name"] = new_feed_data["feed_name"]

        if existing_feed_data["feed_description"] != new_feed_data["feed_description"]:
            data_to_update["feed_description"] = new_feed_data["feed_description"]

        # Using the same author metadata
        data_to_update["created_by"] = existing_feed_data["created_by"]
        data_to_update["created_at"] = existing_feed_data["created_at"]

        # Updating only the editor metadata
        data_to_update["updated_by"] = access_token["user_email"]
        data_to_update["updated_at"] = new_feed_data["updated_at"]

        await feed_collection.update_one(
            {"_id": ObjectId(feed_id)},
            {"$set": data_to_update}
        )

        data_to_return = {
            "feed_id": feed_id,
            "feed_url": f"{GET_FEED_ENDPOINT}{feed_id}",
            "success": True
        }

        return data_to_return

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong! Exited with Exception {e}"
        )