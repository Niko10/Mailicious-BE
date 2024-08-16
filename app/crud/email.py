from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
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
    # Step 2: Get the current email verdicts by modules
    email_verdicts = db.query(Analysis).filter(Analysis.email_id == email_id).all()
    if not email_verdicts:
        raise HTTPException(status_code=404, detail="No verdicts found for the given email ID")
    
    block_decision = False
    alert_decision = False
    for verdict in email_verdicts:
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
    

def get_sender_day_mails_with_link_reputation(sender: str, db: Session):

    today = datetime.now().date()

    try:
        # Query to count distinct receivers for mails with links sent today by the specified sender
        count = (
            db.query(func.count(distinct(Email.recipients)))
            .filter(
                Email.sender == sender,
                func.date(Email.email_datetime) >= today,  # Compare only the date part
                Email.content.op('~')("(https{0,1}\:\/\/\S+|www\.\S+|\S+\.com)[^\w]") 
            )
            .scalar()
        )
        return count

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_sender_day_mails_with_attachment_reputation(sender: str, db: Session):

    today = datetime.now().date()

    try:
        # Query to count distinct receivers for mails with attachments sent today by the specified sender
        count = (
            db.query(func.count(distinct(Email.recipients)))
            .filter(
                Email.sender == sender,
                func.date(Email.email_datetime) >= today,  # Compare only the date part
                func.array_length(Email.attachments, 1) > 0  # Check if attachments array has elements
            )
            .scalar()
        )
        return count

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def sender_domain_reputation(domain: str, db: Session):
    # Calculate the date two weeks ago
    two_weeks_ago = datetime.now().date() - timedelta(weeks=2)

    try:
        # Query to count emails from the specified domain in the last two weeks
        count = (
            db.query(func.count(Email.id))
            .filter(
                Email.sender.like(f"%@{domain}"),  # Match the domain in the sender email
                Email.date >= two_weeks_ago  # Emails sent in the last two weeks
            )
            .scalar()
        )
        return count

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))