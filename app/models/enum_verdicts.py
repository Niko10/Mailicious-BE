from sqlalchemy import Column, Integer, String
from app.db.database import Base

class EnumVerdicts(Base):
    __tablename__ = 'enum_verdicts'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)