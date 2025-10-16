from bson import ObjectId
from fastapi import HTTPException


def verify_original_feed_id(
        id_: str,
        feed_id: str
):
    try:
        original_id = feed_id or id_
        if not original_id:
            raise HTTPException(
                status_code=400,
                detail="Missing feed_id or id parameter"
            )

        if id_:
            try:
                return int(id_)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid legacy feed id: {id_}"
                )

        if feed_id:
            if ObjectId.is_valid(feed_id):
                return ObjectId(feed_id)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid ObjectId: {feed_id}"
                )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail="Feed not found!"
        )
