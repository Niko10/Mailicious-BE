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
    
    print("\nDebuggin get_email_decision ---------------")
    print("received email_id: ", email_id)
    print("received email_id type: ", type(email_id))
    # Step 2: Get the current email verdicts by modules
    email_verdicts = db.query(Analysis).filter(Analysis.email_id == email_id).all()
    if not email_verdicts:
        print("No verdicts found for the given email ID")
        raise HTTPException(status_code=404, detail="No verdicts found for the given email ID")
    
    print("email_verdicts: ", email_verdicts)
    block_decision = False
    alert_decision = False
    for verdict in email_verdicts:
        print("iterating verdict: ")
        for action in actions:
            if verdict.analysis_id == action.module_id and verdict.verdict_id == action.verdict_id:
                if action.block:
                    print(f"for (email_id, verdict_id, module_id) = ({email_id}, {verdict.verdict_id}, {verdict.analysis_id}) block = {action.block}")
                    print(f"for (action_id, verdict_id, module_id) = ({action.id}, {action.verdict_id}, {action.module_id}) block = {action.block}")
                    print("that's why we are blocking the email")
                    block_decision = True  # Block the email
                if action.alert:
                    print(f"for (email_id, verdict_id, module_id) = ({email_id}, {verdict.verdict_id}, {verdict.analysis_id}) alert = {action.alert}")
                    print(f"for (action_id, verdict_id, module_id) = ({action.id}, {action.verdict_id}, {action.module_id}) alert = {action.alert}")
                    print("that's why we are aleritng the email")
                    alert_decision = True

    # update email block and alert correspondingly
    print("block_decision: ", block_decision)
    print("alert_decision: ", alert_decision)
    db_email = db.query(Email).filter(Email.id == email_id).first()
    print("db_email: ", db_email.__dict__)
    db_email.block = block_decision
    db_email.alert = alert_decision
    db.commit()
    db.refresh(db_email)

    print("Debugging ---------------\n")
    return block_decision  # Allow the email


def update_final_verdict(db: Session, email_id: int):
    # step 1: get the analysis for the email
    analyses = db.query(Analysis).filter(Analysis.email_id == email_id).all()
    print("\nDebugging ---------------")
    print("email_id: ", email_id)
    worst_verdict_id = -1
    
    # step 2: find the worst verdict and its corresponding module
    for analysis in analyses:
        print(f"current analysis: {analysis.__dict__}")
        if analysis.verdict_id > worst_verdict_id:
            print(f"worst verdict_id: {worst_verdict_id} -> {analysis.verdict_id} beacuse of module_id: {analysis.analysis_id}")
            worst_verdict_id = analysis.verdict_id
    
    final_verdict_module_id = 1 # should be retrieved from the database

    # step 3: pull the analysis where email_id = email_id and analysis_id = final_verdict_module_id
    final_verdict = db.query(Analysis).filter(Analysis.email_id == email_id, 
                                              Analysis.analysis_id == final_verdict_module_id).first()

    if final_verdict is None:
        print("final verdict is None")
        final_verdict = Analysis(email_id=email_id, analysis_id=final_verdict_module_id, verdict_id=worst_verdict_id)
        db.add(final_verdict)
        db.commit()
        db.refresh(final_verdict)
    else:
        print("current final verdict: ", final_verdict)
        # step 4: update the verdict of the final verdict module
        final_verdict.verdict_id = worst_verdict_id
        db.commit()
        db.refresh(final_verdict)
        print("finished updating the final verdict")
    
    return True
    