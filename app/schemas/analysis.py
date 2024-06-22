from pydantic import BaseModel
from app.schemas.email import Email
from app.schemas.enum_analysis import EnumAnalysis
from app.schemas.enum_verdicts import EnumVerdicts

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
    email: Email
    analysis: EnumAnalysis
    verdict: EnumVerdicts

    class Config:
        orm_mode = True

class Analysis(AnalysisInDBBase):
    pass

class AnalysisInDB(AnalysisInDBBase):
    pass
