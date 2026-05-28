from sqlmodel import SQLModel, Field
from typing import Optional

class ContestProblem(SQLModel, table=True):
    __tablename__ = "contest_problems"
    id: Optional[int] = Field(default=None, primary_key=True, unique=True, nullable=False, index=True)
    problem_id: int = Field(foreign_key="problems.id", nullable=False)
    contest_id: int = Field(foreign_key="contests.id", nullable=False)
    order_num: int = Field(nullable=False, default=0)