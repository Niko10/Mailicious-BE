from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.db.database import Base
import datetime

class Widget(Base):
    __tablename__ = 'widgets'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    config = Column(String)
    name = Column(String)
    type = Column(String)