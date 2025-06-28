import logging

from fastapi import HTTPException
from lxml import etree

from app.controllers.html_to_rss.fetcher_controller import (
    get_static_html_page,
    get_javascript_page
)
from app.schema.html_to_rss import HtmlRssFeedBase


async def parse_input_html(
        xpath_params: HtmlRssFeedBase,
        render_cache_collection
) -> list:
    try:
        xpath_params = xpath_params.model_dump()
        feed_url = xpath_params.get("url")

        if not feed_url:
            raise HTTPException(status_code=400, detail="Bad Request")

        if xpath_params["is_javascript_enabled"] is True:
            source_html = await get_javascript_page(feed_url, render_cache_collection)
        else:
            source_html = await get_static_html_page(feed_url, render_cache_collection)

        html_parser = etree.HTMLParser()
        tree = etree.fromstring(source_html, html_parser)

        items = get_items(tree, xpath_params)

        return items

    except HTTPException as e:
        logging.warning(f"Exited with Exception {e}")
        raise e

    except Exception as e:
        logging.warning(f"Could not parse HTML. Exited with Exception {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error | Exception {e} occurred.")


def get_items(
        tree,
        xpath_params: dict
) -> list:
    items_to_return = []
    items = tree.xpath(xpath_params["item_xpath"])

    for item in items:
        temp_dict = {
            "title": get_individual_field(item, xpath_params["title"]),
            "description": get_individual_field(item, xpath_params["description"]),
            "date": get_individual_field(item, xpath_params["date"]),
            "source_name": xpath_params.get("source_name", "Meltwater"),
            "source_url": xpath_params.get("source_url", "https://app.meltwater.com"),
            "item_url": get_individual_field_with_literals(
                item,
                xpath_params["item_url"],
                xpath_params["item_url_pre_literal"],
                xpath_params["item_url_post_literal"]
            ),
            "image_url": get_image_url(
                item,
                xpath_params["image_url"],
                xpath_params["image_url_pre_literal"],
                xpath_params["image_url_post_literal"],
                xpath_params.get("default_image_url", "")
            )
        }

        items_to_return.append(temp_dict)

    return items_to_return


def get_individual_field(
        item,
        individual_field_xpath: str
) -> str:
    try:
        field_to_return = str(item.xpath(individual_field_xpath)[0])

        if field_to_return.startswith("<Element"):
            logging.warning(f"Skipping unexpected Element: {field_to_return}")
            return ""

    except Exception as e:
        logging.warning(f"Exception {e} while getting field {individual_field_xpath}")
        field_to_return = ""

    return field_to_return


def get_individual_field_with_literals(
        item,
        individual_field_xpath: str,
        individual_field_pre_literal: str = "",
        individual_field_post_literal: str = ""
) -> str:
    try:
        extracted_value = str(item.xpath(individual_field_xpath)[0])
        if extracted_value.startswith("<Element"):
            logging.warning(f"Skipping unexpected Element: {extracted_value}")
            return ""

        field_to_return = (
                individual_field_pre_literal +
                extracted_value +
                individual_field_post_literal
        )
    except Exception as e:
        logging.warning(f"Exception {e} while getting field xpath {individual_field_xpath}")
        field_to_return = (
                individual_field_pre_literal +
                individual_field_post_literal
        )

    return field_to_return


def get_image_url(
        item,
        image_url_xpath: str,
        image_url_pre_literal: str = "",
        image_url_post_literal: str = "",
        default_image_url: str = ""
) -> str:
    try:
        extracted_image_url = str(item.xpath(image_url_xpath)[0])
        if extracted_image_url.startswith("<Element"):
            logging.warning(f"Skipping unexpected Element: {extracted_image_url}")
            raise Exception

        image_url_to_return = (
                image_url_pre_literal +
                extracted_image_url +
                image_url_post_literal
        )
        return image_url_to_return
    except Exception as e:
        logging.warning(f"Exception {e} while getting field xpath {image_url_xpath}")
        return default_image_url or ""
