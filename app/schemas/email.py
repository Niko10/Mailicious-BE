from pydantic import BaseModel, EmailStr, Field, computed_field, validator
from datetime import datetime
from typing import List, Optional, Dict
from app.schemas.enum_modules import EnumModules
from app.schemas.enum_verdicts import EnumVerdicts
import json

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
    SPF_IPs: Optional[str] = Field(default="")
    SPF_status: Optional[str] = Field(default="")
    block: Optional[bool] = False
    alert: Optional[bool] = False

    @validator('subject', 'content', 'attachments', 'SPF_IPs', 'SPF_status', pre=True, always=True)
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

    def __init__(self, **data):
        super().__init__(**data)

    

class EmailSearchResult(EmailInDBBase):
    analyses: Dict[str, str] = {}
    final_verdict: Optional[str] = None

    def __init__(self, **data):
        analyses_data = data.pop('analyses', [])
        super().__init__(**data)
        self.transform_lists_fields_to_list_type()
        self.analyses = self.transform_analyses(analyses_data)
        self.final_verdict = self.compute_final_verdict(analyses_data)

    def transform_lists_fields_to_list_type(self):
        self.recipients = self.recipients.split(",")
        self.attachments = self.attachments.split(",")
        self.SPF_IPs = self.SPF_IPs.split(",")
    
    def transform_analyses(self, analyses: List[Dict]) -> Dict[str, str]:
        transformed_analyses = {}
        for analysis in analyses:
            transformed_analyses[analysis['analysis']['name']] = analysis['verdict']['name']
        return transformed_analyses
    
    def compute_final_verdict(self, analyses: List[Dict]) -> Optional[int]:
        if not analyses:
            return None
        
        final_verdict_id = max(analysis['verdict_id'] for analysis in analyses)
        for analysis in analyses:
            if analysis['verdict_id'] == final_verdict_id:
                final_verdict_name = analysis['verdict']['name']
                break
        return final_verdict_name
                

        
class EmailInSearch(EmailInDBBase):
    pass

class Email(EmailInDBBase):
    pass

class EmailInDB(EmailInDBBase):
    pass
