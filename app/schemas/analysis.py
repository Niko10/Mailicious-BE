from pydantic import BaseModel

class AnalysisBase(BaseModel):
    email_id: int
    analysis_id: int
    verdict_id: int

class AnalysisCreate(AnalysisBase):
    pass

class AnalysisUpdate(AnalysisBase):
    pass

class AnalysisInDBBase(AnalysisBase):
    id: int

    class Config:
        orm_mode = True

class Analysis(AnalysisInDBBase):
    pass

class AnalysisInDB(AnalysisInDBBase):
    pass
