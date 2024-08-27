from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class WidgetFull(BaseModel):
    id: int
    use_id: int 
    config: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None

class WidgetCreate(BaseModel):
    user_id: int 
    config: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None

class WidgetUpdate(BaseModel):
    id: int
    user_id: Optional[int] = None
    config: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None


