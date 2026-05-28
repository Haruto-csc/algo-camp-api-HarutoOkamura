from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from database import engine

from models.users import User
from models.problems import Problem
from models.contests import Contest
from models.contest_problems import ContestProblem

from routers.problems import router as problems_router
from routers.contests import router as contests_router
from routers.users import router as users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(problems_router)
app.include_router(contests_router)
app.include_router(users_router)

@app.get("/")
def read_root():
    return {"status": "FastAPI is running"}