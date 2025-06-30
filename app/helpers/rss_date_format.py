import logging
from datetime import datetime, timezone

from dateutil import parser


def format_to_rss_date(date_input) -> str:
    try:
        # Parse input
        if isinstance(date_input, str):
            dt = parser.isoparse(date_input)
        elif isinstance(date_input, datetime):
            dt = date_input
        else:
            raise TypeError("Unsupported date input type")

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)

        return dt.strftime("%a, %d %b %Y %H:%M:%S %z")

    except Exception as e:
        logging.warning(f"[ERROR] Failed to format RSS date: {date_input} → {e}")
        return ""