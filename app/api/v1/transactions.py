from uuid import UUID
from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
import fastapi
from utils.db_utils import create_database_session
from app.models.data_models import Transaction, FileMetadata
from app.dto.metadata_dto import PaginatedTransactionsResponse, TransactionResponse

router = fastapi.APIRouter()


@router.get("/{file_id}/transactions", response_model=PaginatedTransactionsResponse)
async def get_transactions(
        file_id: UUID,
        category: Optional[str] = Query(None),
        date_from: Optional[date] = Query(None),
        date_to: Optional[date] = Query(None),
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
        db: AsyncSession = Depends(create_database_session),
):
    # Check file exist
    if not await db.get(FileMetadata, file_id):
        raise HTTPException(status_code=404, detail="File not found")

    filters = [Transaction.file_id == file_id]
    if category:
        filters.append(Transaction.category.ilike(f"%{category}%"))
    if date_from:
        filters.append(Transaction.date >= date_from)
    if date_to:
        filters.append(Transaction.date <= date_to)

    total = await db.scalar(select(func.count()).select_from(Transaction).where(and_(*filters)))

    offset = (page - 1) * page_size
    result = await db.execute(
        select(Transaction)
        .where(and_(*filters))
        .order_by(Transaction.date.desc(), Transaction.transaction_id)
        .offset(offset)
        .limit(page_size)
    )
    items = result.scalars().all()

    return PaginatedTransactionsResponse(
        items=[TransactionResponse.from_orm(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size if total else 0,
    )
