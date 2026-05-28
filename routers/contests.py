from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from database import engine
from models import contests
from models.contests import Contest
from pydantic import BaseModel
from models.contest_problems import ContestProblem
from models.problems import Problem
from datetime import datetime, timezone

router = APIRouter(prefix="/contests", tags=["contests"])

def get_db():
    with Session(engine) as session:
        yield session

class ContestCreate(BaseModel):
    title: str
    start_at: datetime
    end_at: datetime
    is_active: bool
    problem_ids: list[int]



@router.get("/{contest_type}")
def read_contests_list(
    contest_type: int,
    db: Session = Depends(get_db)
):
    now = datetime.now(timezone.utc)
    if contest_type == 0:
        statement = select(Contest).where((Contest.is_active == True) & (now < Contest.start_at))
    elif contest_type == 1:
        statement = select(Contest).where((Contest.is_active == True) & (Contest.start_at <= now) & (now <= Contest.end_at))
    elif contest_type == 2:
        statement = select(Contest).where((Contest.is_active == True) & (Contest.end_at < now))
    results = db.exec(statement).all()
    return [
        {"id": c.id, "title": c.title, "start_at": c.start_at, "end_at": c.end_at}
        for c in results
    ]


@router.get("/{contest_id}/contest")
def read_single_contest(contest_id: int, db: Session = Depends(get_db)):
    contest = db.get(Contest, contest_id)
    contest_problem = select(Contest, Problem)
    if not contest:
        raise HTTPException(status_code=404, detail="指定された問題が見つかりません")
    return contest


@router.post("", status_code=201)
def create_problem(
    contest_data: ContestCreate,
    db: Session = Depends(get_db)
):
    # if contest_data.end_time <= contest_data.start_time:
    #     raise HTTPException(
    #         status_code=400,
    #     )
    contest_new_data = contest_data.model_dump()
    problem_ids = contest_new_data.pop("problem_ids")
    new_contest = Contest(**contest_new_data)
    db.add(new_contest)
    # なくてもいいかもだけど一応（重複を通知）
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="コンテスト名が既に存在します")
    db.refresh(new_contest)
    for index, p_id in enumerate(problem_ids):
        assoc = ContestProblem(
            contest_id=new_contest.id,
            problem_id=p_id,
            order_num=index + 1
        )
        db.add(assoc)
    db.commit()
    return new_contest



@router.put("/{contest_id}")
def update_problem(
    contest_id: int,
    updated_data: ContestCreate,
    db: Session = Depends(get_db)
):
    db_contest = db.get(Contest, contest_id)
    if not db_contest:
        raise HTTPException(status_code=404, detail="指定されたコンテストが見つかりません")
    data_dict = updated_data.model_dump()
    problem_ids = data_dict.pop("problem_ids")
    for key, value in data_dict.items():
        setattr(db_contest, key, value)
    db.add(db_contest)
    # contest_problemsを削除
    old_associations = db.exec(
        select(ContestProblem).where(ContestProblem.contest_id == contest_id)
    ).all()
    for old_assoc in old_associations:
        db.delete(old_assoc)
    # contest_problemsを再登録
    for index, p_id in enumerate(problem_ids):
        new_assoc = ContestProblem(
            contest_id=db_contest.id,
            problem_id=p_id,
            order_num=index + 1
        )
        db.add(new_assoc)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="コンテスト名が既に存在します")
    db.refresh(db_contest)
    return db_contest



# 論理削除
@router.delete("/{contest_id}")
def delete_contest(contest_id: int, db: Session = Depends(get_db)):
    contest = db.get(Contest, contest_id)
    if not contest or contest.is_active == False:
        raise HTTPException(status_code=404, detail="指定されたコンテストが見つかりません")
    contest.is_active = False
    db.add(contest)
    db.commit()
    return {"message": "コンテストを削除しました"}

# 物理削除
@router.delete("/{contest_id}/force")
def force_delete_contest(contest_id: int, db: Session = Depends(get_db)):
    contest = db.get(Contest, contest_id)
    if not contest:
        raise HTTPException(status_code=404, detail="指定されたコンテストが見つかりません")
    associations = db.exec(
        select(ContestProblem).where(ContestProblem.contest_id == contest_id)
    ).all()
    for assoc in associations:
        db.delete(assoc)
    db.delete(contest)
    db.commit()
    return #{"message": f"物理削除しました"}

