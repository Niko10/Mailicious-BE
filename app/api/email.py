from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.email import Email, EmailCreate, EmailUpdate
from app.crud import email as crud_email
from app.db.database import get_db
from app.api.auth import get_current_user
from app.schemas.user import User

router = APIRouter()

@router.get("/decision/{email_id}", response_model=bool)
def get_decision(email_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_email.get_email_decision(db, email_id=email_id)

@router.post("/", response_model=Email)
def create_email(email: EmailCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_email.create_email(db=db, email=email)

@router.get("/{email_id}", response_model=Email)
def read_email(email_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_email = crud_email.get_email(db, email_id=email_id)
    if db_email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return db_email

@router.get("/", response_model=List[Email])
def read_emails(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    emails = crud_email.get_emails(db, skip=skip, limit=limit)
    return emails

@router.put("/{email_id}", response_model=Email)
def update_email(email_id: int, email: EmailUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_email = crud_email.get_email(db, email_id=email_id)
    if db_email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return crud_email.update_email(db, db_email=db_email, email_update=email)

@router.delete("/{email_id}", response_model=Email)
def delete_email(email_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_email = crud_email.get_email(db, email_id=email_id)
    if db_email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return crud_email.delete_email(db, email_id=email_id)



@router.get("/get_sender_day_mails_with_link_reputation", response_model=int)
def get_sender_day_mails_with_link_reputation(sender: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_email.get_sender_day_mails_with_link_reputation(db, sender=sender)

@router.get("/get_sender_day_mails_with_attachment_reputation", response_model=int)
def get_sender_day_mails_with_attachment_reputation(sender: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_email.get_sender_day_mails_with_attachment_reputation(db, sender=sender)
    
@router.get("/sender_domain_reputation", response_model=int)

def sender_domain_reputation(domain: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_email.sender_domain_reputation(db, domain=domain)
