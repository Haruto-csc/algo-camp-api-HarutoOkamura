import urllib.parse
from typing import Annotated, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

# 1. パスワードを安全にエンコード
raw_password = "Haruto8610;"
encoded_password = urllib.parse.quote_plus(raw_password)

# 2. 接続URLの組み立て (Transaction Pooler用)
# ユーザー名が postgres.[PROJECT_REF] になっている点に注目
DATABASE_URL = f"postgresql://postgres.hrctlukypdweiqrjnlsx:{encoded_password}@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"

# エンジンの作成
# Poolerを使う場合、コネクションプールが競合しないよう設定を追加するのが安全です
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True  # 接続が切れていないか確認する設定
)