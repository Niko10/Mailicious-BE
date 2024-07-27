from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base
import datetime


class Actions(Base):
    __tablename__ = 'actions'
    
    id = Column(Integer, primary_key=True, index=True)
    created_on = Column(DateTime, index=True, default=datetime.datetime.now())
    module_id = Column(Integer, ForeignKey('enum_modules.id'))
    verdict_id = Column(Integer, ForeignKey('enum_verdicts.id'))
    block: bool = Column(Boolean)
    alert: bool = Column(Boolean)
    
    module = relationship("EnumModules", back_populates="actions")
    verdict = relationship("EnumVerdicts", back_populates="actions")
