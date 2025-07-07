import logging

from bson import ObjectId

from app.controllers.html_to_rss.crud.save_items_controller import save_items
from app.controllers.html_to_rss.parser_controller import parse_input_html
from app.helpers.mongo_doc_serializer import list_mongo_collection_serialize
from app.schema.html_to_rss import HtmlRssFeedBase, HtmlRssFeedRequest
from app.templates.RSS_template import return_rss_output
from app.templates.fallback_RSS_template import get_fallback_rss_output


async def get_rss_feed(
        feed_id: str,
        documents_collection,
        feed_collection,
        render_cache_collection
) -> str:
    try:

        """
        Add logic to get data by parsing for new items and storing in items_collection for now
        """
        feed_metadata = await feed_collection.find_one(
            {"_id": ObjectId(feed_id)},
            {"_id": 0}
        )

        get_items = await parse_input_html(
                HtmlRssFeedBase(**feed_metadata),
                render_cache_collection
        )

        await save_items(
            feed_id,
            get_items,
            documents_collection
        )

        items_from_doc_repo = await documents_collection.find({
            "feed_id": feed_id
        }).to_list(length=None)
        serialized_items = list_mongo_collection_serialize(items_from_doc_repo)

        output_rss_string = return_rss_output(
            HtmlRssFeedRequest(**feed_metadata),
            serialized_items
        )

        return output_rss_string

    except Exception as e:
        logging.warning(f"An Exception {e} occurred while getting feed for ID: {feed_id}")
        return get_fallback_rss_output(feed_id)