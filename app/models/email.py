from sqlalchemy import Column, Integer, String, DateTime, Boolean
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
    SPF_IPs = Column(String)
    SPF_status = Column(String)
    block = Column(Boolean, default=False)
    alert = Column(Boolean, default=False)

    analyses = relationship("Analysis", back_populates="email")
