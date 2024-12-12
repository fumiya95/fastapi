from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "mysql+pymysql://root:root@localhost:3306/fast_api_todo_db"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
#設計図を作成
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        #yieldでfastAPIでDBと高速にやり取りができるようになる
        yield db
    finally:
        db.close()
