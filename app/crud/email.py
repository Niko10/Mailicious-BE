from sqlalchemy.orm import Session
from app.models.email import Email
from app.models.analysis import Analysis
from app.models.actions import Actions
from app.schemas.email import EmailCreate, EmailUpdate
from fastapi import HTTPException

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

def get_email_decision(db: Session, email_id: int):
    actions = db.query(Actions).all()
    if not actions:
        raise HTTPException(status_code=404, detail="No action configurations found")
    
    print("\nDebugging ---------------")
    print("email_id: ", email_id)
    print("actions: ", actions)
    # Step 2: Get the current email verdicts by modules
    email_verdicts = db.query(Analysis).filter(Analysis.email_id == email_id).all()
    if not email_verdicts:
        raise HTTPException(status_code=404, detail="No verdicts found for the given email ID")
    
    print("email_verdicts: ", email_verdicts)
    for verdict in email_verdicts:
        for action in actions:
            if verdict.analysis_id == action.module_id and verdict.verdict_id == action.verdict_id:
                if action.block:
                    print(f"for (email_id, verdict_id, module_id) = ({email_id}, {verdict.verdict_id}, {verdict.analysis_id}) block = {action.block}")
                    print(f"for (action_id, verdict_id, module_id) = ({action.id}, {action.verdict_id}, {action.module_id}) block = {action.block}")
                    print("that's why we are blocking the email")
                    return True  # Block the email

    print("that's why we are allowing the email")
    print("Debugging ---------------\n")
    return False  # Allow the email