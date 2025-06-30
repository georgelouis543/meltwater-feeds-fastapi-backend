def get_fallback_rss_output(
        feed_id: str,
) -> str:
    rss_output = (
        f'<?xml version="1.0" encoding="utf-8"?>\n'
        f'<rss xmlns:media="http://search.yahoo.com/mrss/" version="2.0">\n'
        f'<channel>\n'
        f'<item>\n'
        f'<title>An Error occurred when rendering feed for ID: {feed_id}</title>\n'
        f'</item>\n'
        f'</channel>\n'
        f'</rss>'
    )
    return rss_output
