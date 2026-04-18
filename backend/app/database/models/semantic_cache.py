from sqlalchemy import Column, Integer, Text, DateTime
from pgvector.sqlalchemy import Vector
from datetime import datetime
from backend.app.database.connection import Base

class SemanticCache(Base):
    __tablename__ = "semantic_cache"

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    embedding = Column(Vector(384))
    created_at = Column(DateTime, default=datetime.utcnow)
