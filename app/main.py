import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import PROJECT_NAME, API_V1_STR
from app.routers import router
from app.app_lifespan import lifespan

logger = logging.getLogger('uvicorn')

def create_app() -> CORSMiddleware:
    app = FastAPI(title=PROJECT_NAME, lifespan=lifespan)
    app.include_router(router, prefix=API_V1_STR)

    return CORSMiddleware(
        app,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["POST"],
        allow_headers=["*"],
    )

app = create_app()