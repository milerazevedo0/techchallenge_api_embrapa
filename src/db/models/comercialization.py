from sqlalchemy import Column, DateTime, Integer, String, func
from src.db.base import Base


class ComercializationModel(Base):
    __tablename__ = "comercializations"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    item = Column(String, index=True)
    subitem = Column(String, index=True)
    quantity = Column(Integer)
    importedAt = Column(DateTime, server_default=func.now(), index=True)