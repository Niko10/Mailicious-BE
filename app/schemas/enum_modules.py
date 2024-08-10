from pydantic import BaseModel
from typing import Optional

class EnumModulesBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = True

class EnumModulesCreate(EnumModulesBase):
    pass

class EnumModulesUpdate(EnumModulesBase):
    id: int
    pass

class EnumModulesInDBBase(EnumModulesBase):
    id: int

    class Config:
        orm_mode = True

class EnumModules(EnumModulesInDBBase):
    pass

class EnumModulesInDB(EnumModulesInDBBase):
    pass
