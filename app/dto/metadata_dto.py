from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600


class FileUploadResponse(BaseModel):
    file_id: UUID
    filename: str
    size_bytes: int
    upload_time: datetime
    row_count: int


class FileMetadataResponse(BaseModel):
    id: UUID
    filename: str
    size_bytes: int
    upload_time: datetime
    row_count: int


class CategorySummary(BaseModel):
    category: str
    count: int
    total: Decimal = Field(..., decimal_places=2)


class FileSummaryResponse(BaseModel):
    file_id: UUID
    total_transactions: int
    total_amount: Decimal = Field(..., decimal_places=2)
    currency: str
    date_range: dict[str, date]
    by_category: List[CategorySummary]


class TransactionResponse(BaseModel):
    transaction_id: str
    date: date
    category: str
    amount: Decimal = Field(..., decimal_places=2)
    currency: str

    model_config = ConfigDict(from_attributes=True)


class PaginatedTransactionsResponse(BaseModel):
    items: List[TransactionResponse]
    total: int
    page: int
    page_size: int
    pages: int
