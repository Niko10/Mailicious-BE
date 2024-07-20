from pydantic import BaseModel

class FieldsEnumBase(BaseModel):
    name: str

class FieldsEnumCreate(FieldsEnumBase):
    pass

class FieldsEnumInDBBase(FieldsEnumBase):
    id: int

    class Config:
        orm_mode = True

class FieldsEnum(FieldsEnumInDBBase):
    pass