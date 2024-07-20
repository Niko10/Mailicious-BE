from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base

class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    recipients = Column(String, index=True)
    email_datetime = Column(DateTime, index=True)
    subject = Column(String)
    content = Column(String)
    attachments = Column(String)
    ASNs = Column(String)

    analyses = relationship("Analysis", back_populates="email")
