# algo-camp-api

`algo-camp` のバックエンドAPIアプリケーションです。

## 開発環境 / 技術スタック

- **フレームワーク:** FastAPI 0.136.1
- **言語:** Python 3.13.13
- **ORM / データベース接続:** SQLModel 0.0.38, SQLAlchemy, psycopg2-binary (PostgreSQL)

## ローカル環境での起動方法

### 1. 仮想環境の作成と有効化
プロジェクトのルートディレクトリで、Pythonの仮想環境を作成して有効化します。

# 仮想環境の作成（未作成の場合のみ）
```bash
python -m venv .venv
```

# 仮想環境の有効化（Mac/Linux）
```bash
source .venv/bin/activate
```

### 2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

# 例：PostgreSQLの接続設定（環境に合わせて変更してください）
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/algo_camp_db
```

### 3. 開発サーバーの起動
```bash
fastapi dev
```

サーバーが起動すると、http://localhost:8000 でAPIにアクセスできるようになります。

## APIドキュメント (Swagger UI)
- http://localhost:8000/docs

## ディレクトリ構成

主要なディレクトリと役割の概要です。
```bash
.
├── main.py
├── database.py
├── models/
│   ├── contest_problems.py
│   ├── contests.py
│   ├── problems.py
│   └── users.py
└── routers/
    ├── contests.py
    ├── problems.py
    └── users.py
```