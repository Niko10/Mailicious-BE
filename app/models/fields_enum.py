from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship

class FieldsEnum(Base):
    __tablename__ = 'fields_enum'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    
    blacklists = relationship("Blacklist", back_populates="field")


