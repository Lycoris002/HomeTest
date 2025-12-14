from fastapi import APIRouter, Depends

from app.api.v1.auth import router as auth_api
from app.api.v1.files import router as file_api
from app.api.v1.transactions import router as transaction_api
from middlewares.authentication import verify_token

router = APIRouter()

# Authentication
router.include_router(auth_api, prefix="/auth", tags=["Authentication"])

# File Processing
router.include_router(file_api, prefix="/v1/files", tags=["Files"], dependencies=[Depends(verify_token)])

# Transactions
router.include_router(transaction_api, prefix="/v1/transactions", tags=["Transactions"],
                      dependencies=[Depends(verify_token)])
