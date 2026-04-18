from sqlalchemy import Column, Integer, String, Text, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from backend.app.database.connection import Base
from sqlalchemy import DateTime
from datetime import datetime


class Location(Base):
    __tablename__ = "locations"

    __table_args__ = (
        UniqueConstraint("name", "state"),
    )

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    state = Column(String(50), nullable=False)

    description = Column(Text)

    amenities = Column(JSON)

    url = Column(String(500))

    summary = Column(Text)

    embedding = Column(Vector(384))

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    homes = relationship(
        "Home",
        back_populates="location",
        cascade="all, delete-orphan"
    )

    news_items = relationship(
        "News",
        back_populates="location",
        cascade="all, delete-orphan"
    )

    ads = relationship(
        "Ad",
        back_populates="location",
        cascade="all, delete-orphan"
    )

    releases = relationship(
        "Release",
        back_populates="location",
        cascade="all, delete-orphan"
    )