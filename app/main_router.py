from fastapi import APIRouter
from app.api.v1.files import router as files_router

router = APIRouter()

router.include_router(files_router)