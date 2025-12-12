from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app.api.v1.auth import router as auth_api
from app.api.v1.files import router as file_api
from app.api.v1.transactions import router as transaction_api

router = APIRouter()
bearer_schema = HTTPBearer()

# Authentication
router.include_router(auth_api, tags=["Authentication"])

# File Processing
router.include_router(file_api, tags=["Files"], dependencies=[Depends(bearer_schema)])

# Transactions
router.include_router(transaction_api, tags=["Transactions"], dependencies=[Depends(bearer_schema)])
