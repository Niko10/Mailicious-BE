from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship

class EnumModules(Base):
    __tablename__ = 'enum_modules'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    analyses = relationship("Analysis", back_populates="analysis")
    actions = relationship("Actions", back_populates="module")
