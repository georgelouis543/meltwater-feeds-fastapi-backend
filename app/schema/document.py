import datetime

from pydantic import BaseModel, Field


class ItemDocumentBase(BaseModel):
    feed_id: str = Field(..., description="Manual reference to the feed_id")
    title: str = Field(..., description="This is the article/item title")
    description: str = Field(..., description="An article will have a description (may be optional)")
    published_date: str = Field(default="", description="Published Date")
    item_url: str = Field(..., description="https://www.meltwater.com/slug")
    source_url: str = Field(..., description="https://www.meltwater.com")
    source_name: str = Field(..., description="Meltwater")
    indexed_date: datetime.datetime = Field(
        default=datetime.datetime.now(datetime.UTC),
        description="Timestamp when the item was indexed"
    )


def individual_document_serial(document) -> dict:
    return {
        "_id": str(document["_id"]),
        "feed_id": document["feed_id"],
        "title": document["title"],
        "description": document["title"],
        "published_date": document["published_date"],
        "item_url": document["item_url"],
        "source_url": document["source_url"],
        "source_name": document["source_name"],
        "indexed_date": document["indexed_date"]
    }

def list_documents_serial(docs) -> list:
    return [
        individual_document_serial(doc) for doc in docs
    ]