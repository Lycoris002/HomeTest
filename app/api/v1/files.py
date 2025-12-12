from typing import Annotated
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from utils.db_utils import create_database_session
import fastapi

router = fastapi.APIRouter()


@router.get("/v1/files")
async def get_files():
    pass
