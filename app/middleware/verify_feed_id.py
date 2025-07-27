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
        return original_id

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail="Feed not found!"
        )
