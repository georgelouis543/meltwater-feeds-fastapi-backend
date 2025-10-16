from datetime import datetime
import logging

from app.helpers.date_formats_list import date_fmts


def normalize_date(
        raw_date: str,
        date_regex: str | None = None
) -> str | None:
    if not raw_date or raw_date.strip() == "":
        return None

    if not date_regex or date_regex.strip() == "":
        date_regex = None

    try:
        if date_regex:
            dt = datetime.strptime(raw_date.strip(), date_regex)

        else:
            for fmt in date_fmts:
                try:
                    dt = datetime.strptime(raw_date.strip(), fmt)
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(f"Unknown date format for '{raw_date}'")

        return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")

    except Exception as e:
        logging.warning(f"Could not parse date '{raw_date}' with format '{date_regex}': {e}")
        return None