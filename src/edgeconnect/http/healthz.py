from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/readiness", response_class=PlainTextResponse)
async def readiness() -> str:
    return ""


@router.get("/liveness", response_class=PlainTextResponse)
async def liveness() -> str:
    return ""
