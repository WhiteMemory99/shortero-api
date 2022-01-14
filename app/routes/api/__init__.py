from fastapi import APIRouter

from app.routes.api import short, stats

api_router = APIRouter(prefix="/api")

for module in (short, stats):
    api_router.include_router(module.router)
