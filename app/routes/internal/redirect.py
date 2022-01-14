from fastapi import APIRouter, Depends, HTTPException, status
from short_url import decode_url
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.dependencies.database import get_session
from app.models import Link

router = APIRouter()


@router.get("/{short_id}", response_class=RedirectResponse)
async def resolve_short_link(short_id: str, session: AsyncSession = Depends(get_session)):
    not_found = HTTPException(status.HTTP_404_NOT_FOUND, "This short link doesn't exist")
    try:
        decoded_id = decode_url(short_id)
        link = await session.get(Link, decoded_id)
    except (DBAPIError, ValueError):
        raise not_found

    if link:
        link.clicks += 1
        await session.commit()
        return link.original_url  # Redirect to the original URL

    raise not_found
