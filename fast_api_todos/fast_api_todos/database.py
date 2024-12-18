from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine("#URLを貼り付ける")
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
