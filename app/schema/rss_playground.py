import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class FeedType(str, Enum):
    rss_to_mwfeed = "rss_to_mwfeed"
    rss_to_json = "rss_to_json"
    rss_to_sharepoint = "rss_to_sharepoint"


class RssToMWFeedBase(BaseModel):
    url: str = Field(
        ...,
        description="https://app.meltwater.com/gyda/outputs/669f8b8a824754221e000001/rendering"
                    "?apiKey=57303a640aa4ad579f365861&type=rss"
    )
    is_newsfeed: bool = False # adding this field for aggregation purposes (which might come up in future)
    feed_type: FeedType = Field(default=FeedType.rss_to_mwfeed)
    item_xpath: str = Field(..., description="/rss/channel/item")
    title_xpath: str = Field(..., description=".//title/text()")
    description_xpath: str = Field(..., description=".//description/text()")
    date_regex: str = ""
    date_xpath: str = Field(..., description=".//pubDate/text()")
    use_index_date: bool = False
    item_url_pre_literal: str = ""
    item_url_xpath: str = Field(..., description=".//link/text()")
    item_url_post_literal: str = ""
    source_name: str = Field(..., description="Technikaufsohr")
    source_url: str = Field(..., description="https://technikaufsohr.podigee.io/")
    source_name_xpath: str = Field(..., description=".//source/text()")
    source_url_xpath: str = Field(..., description=".//source/@url")
    image_url_pre_literal: str = ""
    image_url_xpath: str = Field(..., description=".//*[local-name()='thumbnail']/@url")
    image_url_post_literal: str = ""
    default_image_url: str = Field(..., description="https://www.example.com/image1.png")

    @field_validator(
        "source_name",
        mode="before"
    )
    def strip_leading_trailing_spaces(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator(
        "url",
        "item_xpath",
        "title_xpath",
        "description_xpath",
        "date_xpath",
        "item_url_pre_literal",
        "item_url_xpath",
        "item_url_post_literal",
        "source_url",
        "source_name_xpath",
        "source_url_xpath",
        "image_url_pre_literal",
        "image_url_xpath",
        "image_url_post_literal",
        "default_image_url",
        mode="before"
    )
    def remove_all_spaces(cls, v):
        return v.replace(" ", "") if isinstance(v, str) else v


class RssToMWFeedRequest(RssToMWFeedBase):
    feed_name: str = Field(
        default="MWFeed",
        description="Example Feed"
    )
    feed_description: str = Field(
        default="Created by Meltwater Feeds app",
        description="Provide a description for your feed"
    )
    created_by: str = "george.louis@meltwater.com"
    updated_by: str = "george.louis@meltwater.com"
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="Date Created"
    )
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="Date Updated"
    )


class RssToMWFeedRead(RssToMWFeedBase):
    pass


class RssToMWFeedUpdateRequest(RssToMWFeedBase):
    updated_at: datetime.datetime = Field(..., description="Date Updated")
    updated_by: str = "george.louis@meltwater.com"


class RssToMWFeedResponse(BaseModel):
    feed_id: str = Field(..., description="saved feed id")
    feed_url: str = Field(..., description="saved feed URL")
    success: bool = False
