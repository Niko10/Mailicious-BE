# app/schemas/actions.py
from pydantic import BaseModel
from typing import Optional

class ActionBase(BaseModel):
    module_id: int
    verdict_id: int
    block: bool
    alert: bool

    class Config:
        orm_mode = True

class ActionRead(ActionBase):
    id: int

