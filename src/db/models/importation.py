from sqlalchemy import Column, DateTime, Integer, String, func
from src.db.base import Base


class ImportationModel(Base):
    __tablename__ = "importations"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    suboption = Column(String, index=True)
    country = Column(String, index=True)
    quantity = Column(Integer)
    value = Column(Integer)
    importedAt = Column(DateTime, server_default=func.now(), index=True)