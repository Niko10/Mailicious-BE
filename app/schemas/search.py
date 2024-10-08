from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EmailSearchParams(BaseModel):
    sender: Optional[str] = None
    recipients: Optional[str] = None
    content: Optional[str] = None
    from_time: Optional[datetime] = None
    to_time: Optional[datetime] = None

class VerdictSearchParams(BaseModel):
    verdict_id: int
    analysis_id: int

class IntegratedEmailSearchParams(BaseModel):
    id: Optional[list[int]] = None
    sender: Optional[list[str]] = None
    recipients: Optional[list[str]] = None
    content: Optional[list[str]] = None
    subject: Optional[list[str]] = None
    from_time: Optional[datetime] = None
    to_time: Optional[datetime] = None
    text: Optional[str] = None
    verdict: Optional[list[str]] = None
    block: Optional[bool] = None
    alert: Optional[bool] = None
    final_verdict: Optional[list[str]] = None

class GroupBySearch(IntegratedEmailSearchParams):
    group_by_fields: Optional[str] = None
    name: Optional[str] = ""
    type: Optional[str] = ""
    
