from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class SessionBase(BaseModel):
    title: str = Field(..., min_length=1, description="Session title cannot be empty")
    goal: str = Field(..., min_length=1, description="Session goal cannot be empty")
    scheduled_duration: float = Field(..., gt=0, description="Scheduled duration must be positive")

class SessionCreate(SessionBase):
    pass

class InterruptionBase(BaseModel):
    reason: str

class InterruptionCreate(InterruptionBase):
    pass

class Interruption(InterruptionBase):
    id: int
    session_id: int
    pause_time: datetime
    
    class Config:
        from_attributes = True

class Session(SessionBase):
    id: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: str
    created_at: datetime
    interruptions: List[Interruption] = []
    
    class Config:
        from_attributes = True

class SessionUpdate(BaseModel):
    title: Optional[str] = None
    goal: Optional[str] = None
    scheduled_duration: Optional[float] = None

class SessionStart(BaseModel):
    pass

class SessionPause(BaseModel):
    reason: str

class SessionResume(BaseModel):
    pass

class SessionComplete(BaseModel):
    pass

class SessionHistory(BaseModel):
    sessions: List[Session]
    total_sessions: int
    completed_sessions: int
    interrupted_sessions: int
    overdue_sessions: int
    abandoned_sessions: int
    total_productive_time: float  # in minutes
    total_interruptions: int
