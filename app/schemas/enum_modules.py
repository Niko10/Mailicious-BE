from pydantic import BaseModel

class EnumModulesBase(BaseModel):
    name: str
    description: str

class EnumModulesCreate(EnumModulesBase):
    pass

class EnumModulesUpdate(EnumModulesBase):
    pass

class EnumModulesInDBBase(EnumModulesBase):
    id: int

    class Config:
        orm_mode = True

class EnumModules(EnumModulesInDBBase):
    pass

class EnumModulesInDB(EnumModulesInDBBase):
    pass
