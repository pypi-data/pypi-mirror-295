from fastapi import APIRouter
from starlette.responses import FileResponse

from .config import settings

v1_router = APIRouter()


@v1_router.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(path=settings.favicon_path, filename=settings.favicon_path)
