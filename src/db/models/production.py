from sqlalchemy import Column, DateTime, Integer, String, func
from src.db.base import Base


class ProductionModel(Base):
    __tablename__ = "productions"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    item = Column(String, index=True)
    subitem = Column(String, index=True)
    quantity = Column(Integer)
    importedAt = Column(DateTime, server_default=func.now(), index=True)