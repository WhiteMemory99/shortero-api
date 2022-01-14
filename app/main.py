from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.routes.api import api_router
from app.routes.internal import redirect

app = FastAPI(
    title="Shortero API",
    description="A simple API for URL shortening, with click statistics (WIP).",
    version=__version__,
    docs_url=None,
    redoc_url="/api/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(redirect.router, include_in_schema=False)
