from sqlalchemy.orm import Session
from app.models.email import Email
from app.schemas.email import EmailCreate, EmailUpdate

def get_email(db: Session, email_id: int):
    return db.query(Email).filter(Email.id == email_id).first()

def get_emails(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Email).offset(skip).limit(limit).all()

def create_email(db: Session, email: EmailCreate):
    db_email = Email(**email.dict())
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

def update_email(db: Session, db_email: Email, email_update: EmailUpdate):
    for var, value in vars(email_update).items():
        setattr(db_email, var, value) if value else None
    db.commit()
    db.refresh(db_email)
    return db_email

def delete_email(db: Session, email_id: int):
    db_email = db.query(Email).filter(Email.id == email_id).first()
    db.delete(db_email)
    db.commit()
    return db_email
