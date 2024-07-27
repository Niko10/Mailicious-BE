from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
import datetime


class Analysis(Base):
    __tablename__ = 'analysis'
    
    id = Column(Integer, primary_key=True, index=True)
    created_on = Column(DateTime, index=True, default=datetime.datetime.now())
    email_id = Column(Integer, ForeignKey('emails.id'))
    analysis_id = Column(Integer, ForeignKey('enum_modules.id'))
    verdict_id = Column(Integer, ForeignKey('enum_verdicts.id'))
    
    email = relationship("Email", back_populates="analyses")
    analysis = relationship("EnumModules", back_populates="analyses")
    verdict = relationship("EnumVerdicts", back_populates="analyses")
