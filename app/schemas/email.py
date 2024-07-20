from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import List, Optional, Dict
from app.schemas.enum_modules import EnumModules
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
    analysis: EnumModules
    verdict: EnumVerdicts

    class Config:
        orm_mode = True

class EmailBase(BaseModel):
    id: int
    sender: str 
    recipients: str 
    email_datetime: datetime 
    subject: Optional[str] = Field(default="")
    content: Optional[str] = Field(default="")
    attachments: Optional[str] = Field(default="")
    ASNs: Optional[str] = Field(default="")

    @validator('subject', 'content', 'attachments', 'ASNs', pre=True, always=True)
    def set_empty_string_for_none(cls, v):
        return v or ""

class EmailCreate(EmailBase):
    id: Optional[int] = Field(default=None)

class EmailUpdate(EmailBase):
    pass

class EmailInDBBase(EmailBase):
    analyses: List[AnalysisInDBBase] = []
    class Config:
        orm_mode = True

class EmailSearchResult(EmailInDBBase):
    analyses: Dict[str, str] = {}

    def __init__(self, **data):
        analyses_data = data.pop('analyses', [])
        super().__init__(**data)
        self.analyses = self.transform_analyses(analyses_data)

    def transform_analyses(self, analyses: List[Dict]) -> Dict[str, str]:
        transformed_analyses = {}
        for analysis in analyses:
            transformed_analyses[analysis['analysis']['name']] = analysis['verdict']['name']
        return transformed_analyses

class EmailInSearch(EmailInDBBase):
    pass

class Email(EmailInDBBase):
    pass

class EmailInDB(EmailInDBBase):
    pass
