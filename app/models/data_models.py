import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from utils.db_utils import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )
    transaction_id = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False)

    __table_args__ = (
        UniqueConstraint("file_id", "transaction_id", name="uq_file_transaction"),
    )


class FileMetadata(Base):
    __tablename__ = "file_metadata"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    filename = Column(String, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    upload_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    row_count = Column(Integer, nullable=False)
    path = Column(String, nullable=False, unique=True)

    __table_args__ = (UniqueConstraint("path", name="uq_file_path"),)
