from sqlmodel import SQLModel, Field
from typing import Optional

class Problem(SQLModel, table=True):
    __tablename__ = "problems"
    id: Optional[int] = Field(default=None, primary_key=True, unique=True, nullable=False, index=True)
    name: str = Field(unique=True, nullable=False)
    time_limit: int = Field(nullable=False)
    memory_limit: int = Field(nullable=False)
    problem_statement: str = Field(nullable=False, unique=True)
    input_format: str = Field(nullable=False)
    output_format: str = Field(nullable=False)
    test_input_01: str = Field(nullable=False)
    test_output_01: str = Field(nullable=False)
    test_input_02: str = Field(nullable=False)
    test_output_02: str = Field(nullable=False)
    test_input_03: str = Field(nullable=False)
    test_output_03: str = Field(nullable=False)
