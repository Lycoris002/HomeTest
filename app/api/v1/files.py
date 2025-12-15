import os
import csv
import io
from uuid import UUID
from datetime import datetime
from decimal import Decimal
import fastapi
from fastapi import APIRouter, UploadFile, File as FastAPIFile, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from utils.db_utils import create_database_session
from app.models.data_models import FileMetadata, Transaction
from app.dto.metadata_dto import (
    FileUploadResponse,
    FileMetadataResponse,
    FileSummaryResponse,
    CategorySummary,
)

router = fastapi.APIRouter()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
        file: UploadFile = FastAPIFile(...),
        db: AsyncSession = Depends(create_database_session)
):
    if file.content_type not in ["text/csv", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    contents = await file.read()
    size_bytes = len(contents)
    file_id = UUID(os.urandom(16).hex())  # UUID4 random
    upload_dir = "./uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{file_id}_{file.filename}")

    # Parse CSV
    text = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    required_cols = {"transaction_id", "date", "category", "amount", "currency"}
    if not required_cols.issubset(set(reader.fieldnames or [])):
        raise HTTPException(status_code=400, detail="CSV missing required columns")

    transactions = []
    for row in reader:
        transactions.append(Transaction(
            file_id=file_id,
            transaction_id=row["transaction_id"].strip(),
            date=datetime.strptime(row["date"], "%Y-%m-%d"),
            category=row["category"].strip(),
            amount=Decimal(row["amount"]),
            currency=row["currency"].strip(),
        ))

    # Save file
    with open(file_path, "wb") as f:
        f.write(contents)

    # Save DB
    metadata = FileMetadata(
        id=file_id,
        filename=file.filename,
        size_bytes=size_bytes,
        upload_time=datetime.utcnow(),
        row_count=len(transactions),
        path=file_path,
    )

    db.add(metadata)
    db.add_all(transactions)
    await db.commit()
    await db.refresh(metadata)

    return FileUploadResponse(
        file_id=metadata.id,
        filename=metadata.filename,
        size_bytes=metadata.size_bytes,
        upload_time=metadata.upload_time,
        row_count=metadata.row_count,
    )


@router.get("", response_model=list[FileMetadataResponse])
async def list_files(db: AsyncSession = Depends(create_database_session)):
    result = await db.execute(select(FileMetadata).order_by(FileMetadata.upload_time.desc()))
    return result.scalars().all()


@router.get("/{file_id}/summary", response_model=FileSummaryResponse)
async def get_summary(file_id: UUID, db: AsyncSession = Depends(create_database_session)):
    metadata = await db.execute(
        select(FileMetadata).where(FileMetadata.id == file_id)
    )
    if not metadata:
        raise HTTPException(status_code=404, detail="File not found")

    # Aggregates
    total_count = await db.scalar(select(func.count()).select_from(Transaction).where(Transaction.file_id == file_id))
    total_amount = await db.scalar(
        select(func.sum(Transaction.amount)).where(Transaction.file_id == file_id)) or Decimal("0.00")
    currency = await db.scalar(select(Transaction.currency).where(Transaction.file_id == file_id).limit(1))

    date_range_res = await db.execute(
        select(func.min(Transaction.date), func.max(Transaction.date)).where(Transaction.file_id == file_id)
    )
    min_d, max_d = date_range_res.fetchone()
    date_range = {"start": min_d.date() if min_d else None, "end": max_d.date() if max_d else None}

    cat_res = await db.execute(
        select(Transaction.category, func.count(), func.sum(Transaction.amount))
        .where(Transaction.file_id == file_id)
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
    )
    by_category = [
        CategorySummary(category=row[0], count=row[1], total=Decimal(row[2] or 0))
        for row in cat_res.fetchall()
    ]

    return FileSummaryResponse(
        file_id=file_id,
        total_transactions=total_count or 0,
        total_amount=total_amount,
        currency=currency or "UNKNOWN",
        date_range=date_range,
        by_category=by_category,
    )
