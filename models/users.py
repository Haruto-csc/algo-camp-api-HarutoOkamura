from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True, unique=True, nullable=False, index=True)
    name: str = Field(unique=True, nullable=False)
    login_id: str = Field(unique=True, nullable=False, index=True)
    login_password: str = Field(nullable=False)
    is_admin: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": "now()"}
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": "now()", "onupdate": "now()"}
    )
    logined_at: Optional[datetime] = Field(default=None)