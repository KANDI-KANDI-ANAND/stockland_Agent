from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pgvector.sqlalchemy import Vector

from backend.app.database.connection import Base


class Release(Base):

    __tablename__ = "releases"

    id = Column(Integer, primary_key=True, index=True)

    location_id = Column(
        Integer,
        ForeignKey("locations.id", ondelete="CASCADE"),
        nullable=False
    )

    title = Column(String(255))

    status = Column(String(100))

    description = Column(Text)

    link = Column(String(500))

    image_url = Column(String(500))

    summary = Column(Text)

    embedding = Column(Vector(384))

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    location = relationship("Location", back_populates="releases")