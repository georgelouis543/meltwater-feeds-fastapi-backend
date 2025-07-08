import datetime

from pydantic import BaseModel, Field


class DeleteFeedCollectionBase(BaseModel):
    url: str = Field(..., description="https://technikaufsohr.podigee.io/")
    is_javascript_enabled: bool = False
    feed_type: str
    item_xpath: str = Field(..., description="/html/body/div[1]/div/article")
    title_xpath: str = Field(..., description=".//header/h1/a/text()")
    description_xpath: str = Field(..., description=".//section[4]/p/text()")
    date_regex: str = ""
    date_xpath: str = Field(..., description=".//header/time/span/text()")
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
    created_by: str
    created_at: datetime.datetime
    updated_by: str
    updated_at: datetime.datetime
    feed_name: str
    feed_description: str
    deleted_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="Date Deleted"
    )

class DeleteFeedResponse(BaseModel):
    message: str
    success: bool