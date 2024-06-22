from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Analysis(Base):
    __tablename__ = 'analysis'
    
    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey('emails.id'))
    analysis_id = Column(Integer, ForeignKey('enum_analysis.id'))
    verdict_id = Column(Integer, ForeignKey('enum_verdicts.id'))
    
    email = relationship("Email")
    analysis = relationship("EnumAnalysis")
    verdict = relationship("EnumVerdicts")

