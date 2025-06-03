from sqlalchemy import Column, DateTime, Integer, String, func
from src.db.base import Base


class ProcessingModel(Base):
    __tablename__ = "processings"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    suboption = Column(String, index=True)
    item = Column(String, index=True)
    subitem = Column(String, index=True)
    quantity = Column(Integer)
    importedAt = Column(DateTime, server_default=func.now(), index=True)
