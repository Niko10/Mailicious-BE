from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Alert(Base):
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True, index=True)
    rule_name = Column(String, index=True)
    alert_datetime = Column(DateTime)
    email_id = Column(Integer, ForeignKey('emails.id'))
    handled = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    
    email = relationship("Email")
