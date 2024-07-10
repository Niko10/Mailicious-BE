from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class Analysis(BaseModel):
    id: int
    email_id: int
    analysis_id: int
    verdict_id: int

    class Config:
        orm_mode = True

class EmailBase(BaseModel):
    sender: EmailStr
    receiver: EmailStr
    email_datetime: datetime
    content: str

class EmailCreate(EmailBase):
    pass

class EmailUpdate(EmailBase):
    pass

class EmailInDBBase(EmailBase):
    id: int
    analyses: List[Analysis] = []

    class Config:
        orm_mode = True

class Email(EmailInDBBase):
    pass

class EmailInDB(EmailInDBBase):
    pass
