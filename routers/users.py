from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from database import engine
from models.users import User
from pydantic import BaseModel
from datetime import datetime, timezone
# from typing import Optional
# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    with Session(engine) as session:
        yield session

class UserCreate(BaseModel):
    name: str
    login_id: str
    login_password: str
    # is_admin: bool
    # created_at: datetime
    # updated_at: datetime
    # logined_at: Optional[datetime]


@router.get("")
def read_users_list(db: Session = Depends(get_db)):
    statement = select(User.id, User.name, User.login_id, User.login_password)
    results = db.exec(statement).all()

    return [
        {"id": u.id, "name": u.name, "login_id": u.login_id}
        for u in results
    ]

@router.post("", status_code=201)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = User(**user_data.model_dump())
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="アカウント名が既に存在します")
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}")
def update_user(
    user_id: int,
    updated_data: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="アカウントが見つかりません")
    data_dict = updated_data.model_dump()
    for key, value in data_dict.items():
        setattr(db_user, key, value)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="アカウント名が既に存在します")
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="アカウントが見つかりません")
    db.delete(user)
    db.commit()
    return {"message": "アカウントを削除しました"}