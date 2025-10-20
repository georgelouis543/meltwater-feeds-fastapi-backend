from app.helpers.rss_date_format import format_to_rss_date
from app.schema.html_to_rss import HtmlRssFeedRequest
from app.schema.merge_feeds import MergeFeed
from app.schema.rss_playground import RssToMWFeedRequest


def return_rss_output(
        feed_metadata: HtmlRssFeedRequest | RssToMWFeedRequest | MergeFeed,
        items: list,
) -> str:

    feed_metadata = dict(feed_metadata)

    rss_output = ""
    rss_output += f'<?xml version="1.0" encoding="utf-8"?>\n'
    rss_output += f'<rss xmlns:media="http://search.yahoo.com/mrss/" version="2.0">\n'
    rss_output += f'<channel>\n'
    rss_output += f'<title>{feed_metadata.get("feed_title", "")}</title>\n'
    rss_output += f'<description>{feed_metadata.get("feed_description", "")}</description>\n'

    for item in items:
        rss_output += f'<item>\n'
        rss_output += f'<title>{item.get("title")}</title>\n'
        rss_output += f'<source url="{item.get("source_url")}">{item.get("source_name")}</source>\n'
        rss_output += f'<link>{item.get("item_url")}</link>\n'
        rss_output += f'<guid ispermalink="false">{item.get("_id")}</guid>\n'

        if feed_metadata.get("use_index_date", False) is True or not item.get("published_date", None):
            rss_output += f'<pubDate>{format_to_rss_date(str(item.get("indexed_date")))}</pubDate>\n'
        else:
            rss_output += f'<pubDate>{item.get("published_date")}</pubDate>\n'

        rss_output += f'<description>\n'
        rss_output += f'{item.get("description")}\n'
        rss_output += f'</description>\n'
        rss_output += f'<media:content url="{item.get("image_url")}"/>\n'
        rss_output += f'</item>\n'

    rss_output += f'</channel>\n'
    rss_output += f'</rss>\n'

    return rss_output