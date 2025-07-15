from fastapi import HTTPException


def verify_original_feed_id(
        id_: str,
        feed_id: str
):
    original_id = feed_id or id_

    if not original_id:
        raise HTTPException(
            status_code=400,
            detail="Missing feed_id or id parameter"
        )

    return original_id