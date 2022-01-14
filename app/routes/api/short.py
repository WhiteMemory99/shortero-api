from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import PlainTextResponse
from pydantic import HttpUrl
from short_url import encode_url
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import URL

from app.dependencies.database import get_session
from app.models import Link

router = APIRouter(
    tags=["shortening"],
    responses={
        400: {
            "content": {"application/json": {"example": {"detail": "string"}}},
        }
    },
)


def get_encoded_url(base_url: URL, link_id: int) -> str:
    """Encode the link ID using the short_url library."""
    return str(base_url) + encode_url(link_id)


@router.post("/shorten", response_class=PlainTextResponse, status_code=status.HTTP_201_CREATED)
async def create_short_link(
    url: HttpUrl, request: Request, session: AsyncSession = Depends(get_session)
):
    """
    Generate a new short link from the given URL.
    In case an existing URL provided, **this endpoint will return a short link anyway**.
    """
    if request.base_url.hostname == url.host:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "This URL can't be used for shortening")

    result = await session.execute(select(Link.id).filter_by(original_url=url))
    if link_id := result.scalar_one_or_none():
        return get_encoded_url(request.base_url, link_id)

    result = await session.execute(insert(Link).values(original_url=url).returning(Link.id))
    await session.commit()
    return get_encoded_url(request.base_url, result.scalar_one())
