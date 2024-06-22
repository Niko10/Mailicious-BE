from pydantic import BaseModel
from datetime import datetime
from app.schemas.email import Email

class AlertBase(BaseModel):
    rule_name: str
    alert_datetime: datetime
    handled: bool = False
    active: bool = True

class AlertCreate(AlertBase):
    email: Email

class AlertUpdate(AlertBase):
    email: Email

class AlertInDBBase(AlertBase):
    id: int
    email: Email

    class Config:
        orm_mode = True

class Alert(AlertInDBBase):
    pass

class AlertInDB(AlertInDBBase):
    pass
