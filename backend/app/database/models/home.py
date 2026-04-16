from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from pgvector.sqlalchemy import Vector
from backend.app.database.connection import Base


class Home(Base):

    __tablename__ = "homes"

    id = Column(Integer, primary_key=True)

    location_id = Column(Integer, ForeignKey("locations.id"))

    home_type = Column(String(255))

    price = Column(Float)

    bedrooms = Column(Integer)

    bathrooms = Column(Integer)

    size = Column(Float)

    image_url = Column(String(500))

    summary = Column(Text)

    embedding = Column(Vector(384))

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    location = relationship(
        "Location",
        back_populates="homes"
    )
