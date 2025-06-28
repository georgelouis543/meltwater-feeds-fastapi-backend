from pydantic import BaseModel, Field


class HtmlRssFeedBase(BaseModel):
    url: str = Field(..., description="https://technikaufsohr.podigee.io/")
    is_javascript_enabled: bool = False
    item_xpath: str = Field(..., description="/html/body/div[1]/div/article")
    title: str = Field(..., description=".//header/h1/a/text()")
    description: str = Field(..., description=".//section[4]/p/text()")
    date_regex: str = ""
    date: str = Field(..., description=".//header/time/span")
    item_url_pre_literal: str = ""
    item_url: str = Field(..., description=".//header/h1/a/@href")
    item_url_post_literal: str = ""
    source_name: str = Field(..., description="Technikaufsohr")
    source_url: str = Field(..., description="https://technikaufsohr.podigee.io/")
    image_url_pre_literal: str = ""
    image_url: str = ""
    image_url_post_literal: str = ""
    default_image_url: str = Field(..., description="https://www.example.com/image1.png")


class HtmlRssFeedRequest(HtmlRssFeedBase):
    feed_name: str = Field(..., description="Example Feed")
    feed_description: str = Field(..., description="Provide a description for your feed")
    created_by: str = "example@meltwater.com"


class HtmlRssFeedRead(HtmlRssFeedBase):
    pass