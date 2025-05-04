from sqlalchemy import Column, Integer, String
from src.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
