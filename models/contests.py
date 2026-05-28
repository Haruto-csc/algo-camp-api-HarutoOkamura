from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Contest(SQLModel, table=True):
    __tablename__ = "contests"
    id: Optional[int] = Field(default=None, primary_key=True, unique=True, nullable=False, index=True)
    title: str = Field(unique=True, nullable=False)
    start_at: datetime = Field(nullable=False)
    end_at: datetime = Field(nullable=False)
    is_active: bool = Field(nullable=False, default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": "now()"}
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": "now()", "onupdate": "now()"}
    )