import datetime
from enum import Enum

from pydantic import BaseModel, Field

class FeedType(str, Enum):
    merged_feed = "merged_feed"


class MergeFeed(BaseModel):
    feed_ids: list
    feed_type: FeedType = Field(
        default=FeedType.merged_feed
    )
    created_by: str = "george.louis@meltwater.com"
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="Date Created"
    )
    updated_by: str = "george.louis@meltwater.com"
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="Date Updated"
    )
