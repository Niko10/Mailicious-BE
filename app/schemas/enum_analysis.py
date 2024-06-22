from pydantic import BaseModel

class EnumAnalysisBase(BaseModel):
    name: str
    description: str

class EnumAnalysisCreate(EnumAnalysisBase):
    pass

class EnumAnalysisUpdate(EnumAnalysisBase):
    pass

class EnumAnalysisInDBBase(EnumAnalysisBase):
    id: int

    class Config:
        orm_mode = True

class EnumAnalysis(EnumAnalysisInDBBase):
    pass

class EnumAnalysisInDB(EnumAnalysisInDBBase):
    pass
