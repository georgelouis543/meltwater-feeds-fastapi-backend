import datetime
import logging
import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()
PHANTOM_JS_API_URL = os.getenv("PHANTOM_JS_URL")

async def get_javascript_page(url: str, render_cache_collection) -> str:
    try:
        # Check if the source has been cached for the given URL
        is_cached = await render_cache_collection.find_one({
            "url": url
        })
        if is_cached:
            logging.info(f"Found Cache. Returning Cached HTML for the URL: {url}")
            return is_cached["html"]

        payload = {
            "url": url,
            "renderType": "html",
            "overseerScript": (
                "await page.waitForNavigation("
                "{waitUntil:\"networkidle0\", timeout:30000}"
                "); page.done();"
            ),
            "outputAsJson": True
        }

        headers = {
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                PHANTOM_JS_API_URL,
                json=payload,
                headers=headers
            )
            response.raise_for_status()

            result = response.json()

            await render_cache_collection.insert_one({
                "url": url,
                "html": result["content"]["data"],
                "cached_at": datetime.datetime.now(datetime.UTC)
            })


            return result["content"]["data"]

    except httpx.HTTPStatusError as e:
        logging.warning(f"Could not fetch source. Exited with HTTPStatusError: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching Source. Exception {e} occurred")

    except httpx.RequestError as e:
        logging.warning(f"Could not fetch source. Exited with RequestError: {e}")
        raise HTTPException(status_code=404, detail=f"Error fetching Source. Exception {e} occurred")

    except Exception as e:
        logging.warning(f"Could not fetch source. Exited with Exception: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching Source. Exception {e} occurred")



async def get_static_html_page(url: str, render_cache_collection) -> str:
    try:
        # Check if the source has been cached for the given URL
        is_cached = await render_cache_collection.find_one({
            "url": url
        })
        if is_cached:
            logging.info(f"Found Cache. Returning Cached HTML for the URL: {url}")
            return is_cached["html"]


        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url)
            response.raise_for_status()

            result = response.text

            await render_cache_collection.insert_one({
                "url": url,
                "html": result,
                "cached_at": datetime.datetime.now(datetime.UTC)
            })


            return result

    except httpx.HTTPStatusError as e:
        logging.warning(f"Could not fetch source. Exited with HTTPStatusError: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching Source. Exception {e} occurred")

    except httpx.RequestError as e:
        logging.warning(f"Could not fetch source. Exited with RequestError: {e}")
        raise HTTPException(status_code=404, detail=f"Error fetching Source. Exception {e} occurred")

    except Exception as e:
        logging.warning(f"Could not fetch source. Exited with Exception: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching Source. Exception {e} occurred")