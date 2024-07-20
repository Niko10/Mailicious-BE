from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.email import Email
from app.models.analysis import Analysis

def search_emails(db: Session, params: dict):
    print("[DEBUG] search_emails - Params:", params)

    query = db.query(Email)

    if params.get("senders"):
        senders = params["senders"].split(",")
        senders = [sender.strip() for sender in senders]  # Strip whitespace
        sender_conditions = [Email.sender.ilike(f"%{sender}%") for sender in senders]
        query = query.filter(or_(*sender_conditions))
        print("[DEBUG] Added sender conditions:", sender_conditions)

    if params.get("recipients"):
        recipients = params["recipients"].split(",")
        recipients = [recipient.strip() for recipient in recipients]  # Strip whitespace
        recipient_conditions = [Email.recipients.ilike(f"%{recipient}%") for recipient in recipients]
        query = query.filter(or_(*recipient_conditions))
        print("[DEBUG] Added recipient conditions:", recipient_conditions)

    if params.get("content"):
        query = query.filter(Email.content.ilike(f"%{params['content']}%"))
        print("[DEBUG] Added content condition:", params['content'])

    if params.get("from_time"):
        query = query.filter(Email.email_datetime >= params["from_time"])
        print("[DEBUG] Added from_time condition:", params['from_time'])

    if params.get("to_time"):
        query = query.filter(Email.email_datetime <= params["to_time"])
        print("[DEBUG] Added to_time condition:", params['to_time'])

    print("[DEBUG] Final Query:", str(query))
    return query.order_by(Email.email_datetime.desc()).all()

def search_by_verdict(db: Session, verdict_id: int, analysis_id: int):
    print("[DEBUG] search_by_verdict - Verdict ID:", verdict_id, "Analysis ID:", analysis_id)
    query = db.query(Email).join(Analysis, Analysis.email_id == Email.id).filter(
        and_(Analysis.verdict_id == verdict_id, Analysis.analysis_id == analysis_id)
    )

    print("[DEBUG] search_by_verdict - Query:", str(query))
    return query.order_by(Email.email_datetime.desc()).all()


def search_emails_by_text(db: Session, text: str):
    print("[DEBUG] search_emails_by_text - Text:", text)
    query = db.query(Email).filter(
        or_(
            Email.sender.ilike(f"%{text}%"),
            Email.recipients.ilike(f"%{text}%"),
            Email.content.ilike(f"%{text}%"),
            Email.subject.ilike(f"%{text}%"),
            Email.attachments.ilike(f"%{text}%"),
            Email.ASNs.ilike(f"%{text}%")
        )
    )

    print("[DEBUG] search_emails_by_text - Query:", str(query))
    return query.order_by(Email.email_datetime.desc()).all()