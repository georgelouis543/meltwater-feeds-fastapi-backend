import logging


async def get_feeds_handler(feed_collection):
    try:
        feeds_cursor = feed_collection.find()
        feeds_raw = await feeds_cursor.to_list(length=None)

        # Serializing in the same function for testing. Do it later in the schema module
        feeds = []
        for feed in feeds_raw:
            feed["_id"] = str(feed["_id"])
            feeds.append(feed)

        return feeds

    except Exception as e:
        logging.warning(f"Exception while retrieving all feeds: {e}")
        return []