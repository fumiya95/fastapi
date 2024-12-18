from sqlalchemy import Column, Integer,String,DateTime,Boolean,Text,ForeignKey
from database import Base
from datetime import datetime

class Todos(Base):
    #テーブルの指定
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False,)
    description = Column(Text, nullable=False,)
    priority = Column(Integer)
    complete = Column(Boolean)
    created_at = Column(DateTime,default=datetime.now())
    updated_at = Column(DateTime,default=datetime.now(),onupdate=datetime.now())

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String(255))

class Todos(Base):
    __tablename__ = "todos"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, )
    description = Column(Text, nullable=True)
    priority = Column(Integer)
    complete = Column(Boolean)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    user_id = Column(Integer, ForeignKey("users.id"))
