from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from database import engine
from models.problems import Problem
from pydantic import BaseModel

router = APIRouter(prefix="/problems", tags=["problems"])

def get_db():
    with Session(engine) as session:
        yield session

class ProblemCreate(BaseModel):
    name: str
    time_limit: int
    memory_limit: int
    problem_statement: str
    input_format: str
    output_format: str
    test_input_01: str
    test_output_01: str
    test_input_02: str
    test_output_02: str
    test_input_03: str
    test_output_03: str

@router.get("")
def read_problems_list(db: Session = Depends(get_db)):
    statement = select(Problem.id, Problem.name, Problem.time_limit, Problem.memory_limit)
    results = db.exec(statement).all()
    return [
        {"id": p.id, "name": p.name, "time_limit": p.time_limit, "memory_limit": p.memory_limit}
        for p in results
    ]

@router.get("/{problem_id}")
def read_single_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="指定された問題が見つかりません")
    return problem

@router.post("", status_code=201)
def create_problem(
    problem_data: ProblemCreate,
    db: Session = Depends(get_db)
):
    new_problem = Problem(**problem_data.model_dump())
    db.add(new_problem)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="問題名が既に存在します")
    db.refresh(new_problem)
    return new_problem

@router.put("/{problem_id}")
def update_problem(
    problem_id: int,
    updated_data: ProblemCreate,
    db: Session = Depends(get_db)
):
    db_problem = db.get(Problem, problem_id)
    if not db_problem:
        raise HTTPException(status_code=404, detail="指定された問題が見つかりません")
    data_dict = updated_data.model_dump()
    for key, value in data_dict.items():
        setattr(db_problem, key, value)
    db.add(db_problem)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="問題名が既に存在します")
    db.refresh(db_problem)
    return db_problem

@router.delete("/{problem_id}")
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="指定された問題が見つかりません")
    db.delete(problem)
    db.commit()
    return {"message": "問題を削除しました"}