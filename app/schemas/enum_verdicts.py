from pydantic import BaseModel

class EnumVerdictsBase(BaseModel):
    name: str
    description: str

class EnumVerdictsCreate(EnumVerdictsBase):
    pass

class EnumVerdictsUpdate(EnumVerdictsBase):
    pass

class EnumVerdictsInDBBase(EnumVerdictsBase):
    id: int

    class Config:
        orm_mode = True

class EnumVerdicts(EnumVerdictsInDBBase):
    pass

class EnumVerdictsInDB(EnumVerdictsInDBBase):
    pass
