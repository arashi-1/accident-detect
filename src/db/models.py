from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class AccidentEvent(Base):
    __tablename__ = "accident_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    location_lat = Column(Float, nullable=True)
    location_lng = Column(Float, nullable=True)
    severity = Column(String, default="unknown")
    score = Column(Float, nullable=False)
    clip_path = Column(String, nullable=True)  # path to saved video snippet
    alert_status = Column(String, default="pending")  # pending/sent/failed
