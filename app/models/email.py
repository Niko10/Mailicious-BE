from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base

class Email(Base):
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    receiver = Column(String, index=True)
    email_datetime = Column(DateTime)
    content = Column(String)
