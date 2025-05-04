from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.base import Base
import os

# Caminho para o banco SQLite
DATABASE_URL = "sqlite:///./user.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from src.db.models import user  # Importa os models
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()