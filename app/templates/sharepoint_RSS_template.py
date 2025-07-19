from app.helpers.rss_date_format import format_to_rss_date
from app.schema.html_to_rss import HtmlRssFeedRequest
from app.schema.rss_playground import RssToMWFeedRequest


def return_sharepoint_rss_output(
        feed_metadata: HtmlRssFeedRequest | RssToMWFeedRequest,
        items: list,
) -> str:

    feed_metadata = dict(feed_metadata)

    rss_output = ""
    rss_output += f'<?xml version="1.0" encoding="utf-8"?>\n'
    rss_output += (f'<rss xmlns:dc="http://purl.org/dc/elements/1.1/" '
                   f'xmlns:media="http://search.yahoo.com/mrss/ version="2.0">\n')
    rss_output += f'<channel>\n'
    rss_output += f'<title>{feed_metadata["feed_name"]}</title>\n'
    rss_output += f'<description>{feed_metadata["feed_description"]}</description>\n'
    rss_output += f'<language>en-us</language>\n'

    for item in items:
        rss_output += f'<item>\n'
        rss_output += f'<title>{item["title"]}</title>\n'
        rss_output += f'<source url="{item["source_url"]}">{item["source_name"]}</source>\n'
        rss_output += f'<link>{item["item_url"]}</link>\n'
        rss_output += f'<guid ispermalink="true">{item["_id"]}</guid>\n'

        if feed_metadata["use_index_date"] is True or not item["published_date"]:
            rss_output += f'<pubDate>{format_to_rss_date(str(item["indexed_date"]))}</pubDate>\n'
        else:
            rss_output += f'<pubDate>{item["published_date"]}</pubDate>\n'

        rss_output += f'<description>\n'
        rss_output += f'{item["description"]}\n'
        rss_output += f'</description>\n'
        rss_output += f'<media:thumbnail url="{item["image_url"]}"/>\n'
        rss_output += f'</item>\n'

    rss_output += f'</channel>\n'
    rss_output += f'</rss>\n'

    return rss_output