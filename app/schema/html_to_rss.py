import datetime
from enum import Enum

from pydantic import (
    BaseModel,
    Field,
    field_validator
)


class FeedType(str, Enum):
    html_to_rss = "html_to_rss"


class HtmlRssFeedBase(BaseModel):
    url: str = Field(..., description="https://technikaufsohr.podigee.io/")
    is_javascript_enabled: bool = False
    feed_type: FeedType = Field(default=FeedType.html_to_rss)
    item_xpath: str = Field(..., description="/html/body/div[1]/div/article")
    title_xpath: str = Field(..., description=".//header/h1/a/text()")
    description_xpath: str = Field(..., description=".//section[4]/p/text()")
    date_regex: str = ""
    date_xpath: str = Field(..., description=".//header/time/span")
    use_index_date: bool = False
    item_url_pre_literal: str = ""
    item_url_xpath: str = Field(..., description=".//header/h1/a/@href")
    item_url_post_literal: str = ""
    source_name: str = Field(..., description="Technikaufsohr")
    source_url: str = Field(..., description="https://technikaufsohr.podigee.io/")
    image_url_pre_literal: str = ""
    image_url_xpath: str = ""
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
        "image_url_pre_literal",
        "image_url_xpath",
        "image_url_post_literal",
        "default_image_url",
        mode="before"
    )
    def remove_all_spaces(cls, v):
        return v.replace(" ", "") if isinstance(v, str) else v


class HtmlRssFeedRequest(HtmlRssFeedBase):
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


class HtmlRssFeedRead(HtmlRssFeedBase):
    pass


class HtmlRssFeedUpdateRequest(HtmlRssFeedBase):
    updated_at: datetime.datetime = Field(..., description="Date Updated")
    updated_by: str = "george.louis@meltwater.com"


class HtmlRssFeedResponse(BaseModel):
    feed_id: str = Field(..., description="saved feed id")
    feed_url: str = Field(..., description="saved feed URL")
    success: bool = False
