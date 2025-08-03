import logging

from fastapi import HTTPException

from app.schema.document import ItemDocumentBase


async def save_items(
        feed_id: str,
        items: list[dict],
        documents_collection
):
    try:
        existing_items_cursor = documents_collection.find(
            {
                "feed_id": feed_id
            },
            {
                "_id": 0,
                "title": 1
            }
        )
        existing_items = await existing_items_cursor.to_list(length=None)

    except Exception as e:
        logging.warning(f"An Exception {e} occurred while retrieving existing documents")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error. "
                   f"An Exception {e} occurred while retrieving existing documents"
        )

    # Use set for constant O(1) lookup
    existing_titles = {
        existing_item["title"] for existing_item in existing_items
    }

    documents_to_insert = []

    for item in items:
        try:
            if item["title"] not in existing_titles:
                # Validate item using Pydantic
                document = ItemDocumentBase(
                    **item,
                    feed_id=feed_id
                )

                documents_to_insert.append(document.model_dump())

        except Exception as e:
            logging.warning(f"Skipping item due to error: {e}")
            continue

    if documents_to_insert:
        try:
            await documents_collection.insert_many(documents_to_insert)
        except Exception as e:
            logging.warning(f"Exception {e} occurred while adding documents to the Doc Repo")
            raise HTTPException(
                status_code=500,
                detail=f"Exception {e} occurred. Could not add documents"
            )
