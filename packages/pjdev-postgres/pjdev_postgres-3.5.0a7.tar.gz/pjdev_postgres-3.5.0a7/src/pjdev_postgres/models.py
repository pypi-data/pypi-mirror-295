from datetime import datetime, UTC
from typing import Optional, Annotated
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Index

from pjdev_postgres.model_validators import date_validator


class ConnectionOptions(BaseModel):
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10


class Versioned(BaseModel):
    concurrency_token: Optional[UUID] = None


class Auditable(BaseModel):
    created_by_id: Optional[str] = None
    created_by: Optional[str] = None
    created_datetime: Annotated[
        datetime, date_validator, Field(default_factory=lambda: datetime.now(UTC))
    ]
    last_modified_by_id: Optional[str] = None
    last_modified_by: Optional[str] = None
    last_modified_datetime: Annotated[Optional[datetime], date_validator] = None


class TableModel(SQLModel):
    row_id: Optional[int] = Field(default=None, primary_key=True)


class Savable(Versioned, Auditable, TableModel):
    pass


class History(TableModel, table=True):
    entity_name: str
    entity_id: int
    value: str
    timestamp: Annotated[
        datetime, date_validator, Field(default_factory=lambda: datetime.now(UTC))
    ]

    __table_args__ = (
        Index("ix_history_entity_id", "entity_id"),
        Index("ix_history_entity_name", "entity_name"),
        Index("ix_history_timestamp", "timestamp"),
    )


class ConcurrencyException(BaseException):
    def __init__(self, message: str):
        super().__init__(message)
