from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.app.database.connection import Base


class Interest(Base):

    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))

    community = Column(String(200))
    message = Column(String(500))

    created_at = Column(DateTime, default=datetime.utcnow)