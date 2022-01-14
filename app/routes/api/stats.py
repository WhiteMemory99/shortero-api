from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import HttpUrl
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schema
from app.dependencies.database import get_session
from app.models import Link

router = APIRouter(
    tags=["stats"],
    responses={
        404: {
            "content": {"application/json": {"example": {"detail": "string"}}},
        }
    },
)


@router.post("/stats", response_model=schema.OutLink)
async def get_link_stats(
    url: HttpUrl = Query(..., description="A raw URL to the original website"),
    session: AsyncSession = Depends(get_session),
):
    """
    Get some statistics on the given URL, like **clicks count**.
    Only works for URLs that already have shortened version.
    """
    result = await session.execute(select(Link).filter_by(original_url=url))
    if link := result.scalar_one_or_none():
        return link

    raise HTTPException(status.HTTP_404_NOT_FOUND, "This URL doesn't have a short link")
