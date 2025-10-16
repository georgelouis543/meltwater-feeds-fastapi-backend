import logging
import os

import httpx
from dotenv import load_dotenv

load_dotenv()
LEGACY_GET_ENDPOINT = os.getenv("LEGACY_GET_FEED_ENDPOINT")

async def redirect_to_legacy_feed(
        feed_id: str
):
    feed_id = int(feed_id)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{LEGACY_GET_ENDPOINT}{feed_id}")
            response.raise_for_status()
            return response.content

    except httpx.RequestError as e:
        logging.warning(f"Error while requesting legacy server: {e}")

    except httpx.HTTPStatusError as e:
        logging.warning(
            f"Legacy server returned an error response {e.response.status_code}: {e.response.text}"
        )

    except Exception as e:
        logging.warning(f"Error while requesting legacy server: {e}")

    return None



