from pydantic import BaseModel, EmailStr
from datetime import datetime

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

    class Config:
        orm_mode = True

class Email(EmailInDBBase):
    pass

class EmailInDB(EmailInDBBase):
    pass
