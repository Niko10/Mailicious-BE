from pydantic import BaseModel
from typing import Optional, Dict
from app.schemas.fields_enum import FieldsEnum

class BlacklistBase(BaseModel):
    value: str

class BlacklistCreate(BlacklistBase):
    field_id: int

class BlacklistInDBBase(BlacklistBase):
    id: int
    field: FieldsEnum

    class Config:
        orm_mode = True

class Blacklist(BlacklistInDBBase):
    pass

class BlacklistGrouped(BaseModel):
    field_id: int
    field_name: str
    values: str