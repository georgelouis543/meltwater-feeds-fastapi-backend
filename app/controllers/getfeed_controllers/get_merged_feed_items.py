import asyncio
import logging


async def fetch_items(
        feed_id: str,
        documents_collection
):
    try:
        items = await documents_collection.find({
            "feed_id": str(feed_id)
        }).to_list(length=None)
        for item in items:
            item["_id"] = str(item["_id"])

        return items

    except Exception as e:
        logging.warning(f"Error fetching feed {feed_id}: {e}")
        return []


async def get_merged_items_handler(
        feed_ids: list,
        documents_collection,
) -> list:
    try:
        results = await asyncio.gather(
            *(fetch_items(feed_id, documents_collection) for feed_id in feed_ids)
        )
        merged_items = [
            item for sublist in results for item in sublist
        ]

        return merged_items

    except Exception as e:
        logging.error(f"Exception: {e} occurred while merging feeds!")
        return []


