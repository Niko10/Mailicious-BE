from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.email import Email
from app.models.analysis import Analysis
import json

DEBUG_MSG_PREFIX = "./app/crud/search.py -"

def search_emails(db: Session, params: dict):
    debug_msg_current = f"{DEBUG_MSG_PREFIX} search_emails"
    print(f"[DEBUG] {debug_msg_current} - Params:\n", params)

    query = db.query(Email)

    if params.get("sender"):
        senders = params["sender"]
        senders = [sender.strip() for sender in senders]  # Strip whitespace
        sender_conditions = [Email.sender.ilike(f"%{sender}%") for sender in senders]
        query = query.filter(or_(*sender_conditions))

    if params.get("recipients"):
        recipients = params["recipients"]
        recipients = [recipient.strip() for recipient in recipients]  # Strip whitespace
        recipient_conditions = [Email.recipients.ilike(f"%{recipient}%") for recipient in recipients]
        query = query.filter(or_(*recipient_conditions))

    if params.get("content"):
        contents = params["content"]
        content_conditions = [Email.content.ilike(f"%{content}%") for content in contents]
        query = query.filter(or_(*content_conditions))

    if params.get("subject"):
        subjects = params["subject"]
        subject_conditions = [Email.subject.ilike(f"%{subject}%") for subject in subjects]
        query = query.filter(or_(*subject_conditions))

    if params.get("from_time"):
        query = query.filter(Email.email_datetime >= params["from_time"])

    if params.get("to_time"):
        query = query.filter(Email.email_datetime <= params["to_time"])

    print(f"[DEBUG] {debug_msg_current} Final Query: ", str(query))
    return query.order_by(Email.email_datetime.desc()).all()

def search_by_verdict(db: Session, verdict_id: int, analysis_id: int):
    debug_msg_current = f"{DEBUG_MSG_PREFIX} search_by_verdict"
    print(f"[DEBUG] {debug_msg_current} - Verdict ID:", verdict_id, "Analysis ID:", analysis_id)
    query = db.query(Email).join(Analysis, Analysis.email_id == Email.id).filter(
        and_(Analysis.verdict_id == verdict_id, Analysis.analysis_id == analysis_id)
    )

    print(f"[DEBUG] {debug_msg_current} - Query: ", str(query))
    return query.order_by(Email.email_datetime.desc()).all()


def search_emails_by_text(db: Session, text: str):
    debug_msg_current = f"{DEBUG_MSG_PREFIX} search_emails_by_text"
    print(f"[DEBUG] {debug_msg_current} - Text:", text)
    query = db.query(Email).filter(
        or_(
            Email.sender.ilike(f"%{text}%"),
            Email.recipients.ilike(f"%{text}%"),
            Email.content.ilike(f"%{text}%"),
            Email.subject.ilike(f"%{text}%"),
            Email.attachments.ilike(f"%{text}%"),
            Email.SPF_IPs.ilike(f"%{text}%"),
            Email.SPF_status.ilike(f"%{text}%")
        )
    )

    print(f"[DEBUG] {debug_msg_current} search_emails_by_text - Query: ", str(query))
    return query.order_by(Email.email_datetime.desc()).all()