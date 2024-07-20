from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship

class Blacklist(Base):
    __tablename__ = 'blacklist'
    
    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey('fields_enum.id'))
    value = Column(String)
    
    field = relationship("FieldsEnum", back_populates="blacklists")