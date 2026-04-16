from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pgvector.sqlalchemy import Vector

from backend.app.database.connection import Base


class News(Base):

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)

    location_id = Column(
        Integer,
        ForeignKey("locations.id", ondelete="CASCADE"),
        nullable=False
    )

    title = Column(String(255))

    summary = Column(Text)

    content = Column(Text)

    link = Column(String(500))

    published_date = Column(String(50))

    embedding = Column(Vector(384))

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    location = relationship(
        "Location",
        back_populates="news_items"
    )