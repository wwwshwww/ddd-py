from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# DBセッションを作成する依存関係
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# 例: ユーザを取得するエンドポイント
@app.get("/users/{user_id}")
async def read_user(user_id: int, db=Annotated[Session, Depends(get_db)]):
    # ここでDB操作を行う
    # 例えば、db.query(User).filter(User.id == user_id).first() のように
    print(user_id)
    print(db)
    return user_id
