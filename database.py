import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session  # 👈 SQLModelから読み込むように変更

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def get_session():
    with Session(engine) as session:
        yield session