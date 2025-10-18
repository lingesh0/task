from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    goal = Column(Text, nullable=False)
    scheduled_duration = Column(Float, nullable=False)  # in minutes
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    status = Column(String(50), default="planned")  # planned, active, paused, completed, interrupted, overdue, abandoned
    created_at = Column(DateTime, default=func.now())
    
    # Relationship to interruptions
    interruptions = relationship("Interruption", back_populates="session", cascade="all, delete-orphan")

class Interruption(Base):
    __tablename__ = "interruptions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    reason = Column(Text, nullable=False)
    pause_time = Column(DateTime, default=func.now())
    
    # Relationship back to session
    session = relationship("Session", back_populates="interruptions")
