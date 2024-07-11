from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EmailSearchParams(BaseModel):
    sender: Optional[str] = None
    receiver: Optional[str] = None
    content: Optional[str] = None
    from_time: Optional[datetime] = None
    to_time: Optional[datetime] = None

class VerdictSearchParams(BaseModel):
    verdict_id: int
    analysis_id: int

class IntegratedEmailSearchParams(BaseModel):
    sender: Optional[str] = None
    receiver: Optional[str] = None
    content: Optional[str] = None
    from_time: Optional[datetime] = None
    to_time: Optional[datetime] = None
    text: Optional[str] = None
    verdict_id: Optional[int] = None
    
