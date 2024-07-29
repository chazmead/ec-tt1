import logging

from fastapi import FastAPI

from edgeconnect import config
from edgeconnect.http import commodities, healthz, middlewares

logger = logging.getLogger(__name__)

api = FastAPI()

# Middlewares
api.add_middleware(
    middlewares.StandardErrorResponse,
    debug_mode=config.DEBUG,
    logger=logger,
)

# Routers
api.include_router(healthz.router, prefix="/healthz")
api.include_router(commodities.router, prefix=config.ROOT_URI_PATH)
