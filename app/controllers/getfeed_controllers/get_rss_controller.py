import logging

from bson import ObjectId
from fastapi import HTTPException

from app.controllers.legacy_feeds.serve_legacy_feed import redirect_to_legacy_feed
from app.helpers.mongo_doc_serializer import list_mongo_collection_serialize
from app.schema.html_to_rss import HtmlRssFeedRequest
from app.schema.rss_playground import RssToMWFeedRequest
from app.templates.RSS_template import return_rss_output
from app.templates.fallback_RSS_template import get_fallback_rss_output
from app.templates.sharepoint_RSS_template import return_sharepoint_rss_output


async def get_rss_feed(
        feed_id,
        documents_collection,
        feed_collection
) -> str:
    try:
        feed_metadata = await feed_collection.find_one(
            {"_id": feed_id},
            {"_id": 0}
        )

        if not feed_metadata:
            raise HTTPException(status_code=404, detail="Feed Not found!")

        if feed_metadata["feed_type"] == "legacy_feed":
            response = await redirect_to_legacy_feed(feed_id)
            return response if response else get_fallback_rss_output(feed_id)

        items_from_doc_repo = await documents_collection.find({
            "feed_id": str(feed_id)
        }).to_list(length=None)
        serialized_items = list_mongo_collection_serialize(
            items_from_doc_repo
        )

        output_rss_string = ""

        if feed_metadata["feed_type"] == "html_to_rss":
            output_rss_string = return_rss_output(
                HtmlRssFeedRequest(**feed_metadata),
                serialized_items
            )

        elif feed_metadata["feed_type"] == "rss_to_mwfeed":
            output_rss_string = return_rss_output(
                RssToMWFeedRequest(**feed_metadata),
                serialized_items
            )

        elif feed_metadata["feed_type"] == "rss_to_sharepoint":
            # Add sharepoint template call here
            output_rss_string = return_sharepoint_rss_output(
                RssToMWFeedRequest(**feed_metadata),
                serialized_items
            )

        return output_rss_string

    except Exception as e:
        logging.warning(f"An Exception {e} occurred while getting feed for ID: {feed_id}")
        return get_fallback_rss_output(feed_id)