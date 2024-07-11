from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.email import Email
from app.models.analysis import Analysis

def search_emails(db: Session, params: dict):
    query = db.query(Email)

    if params.get("sender"):
        query = query.filter(Email.sender.ilike(f"%{params['sender']}%"))
    if params.get("receiver"):
        query = query.filter(Email.receiver.ilike(f"%{params['receiver']}%"))
    if params.get("content"):
        query = query.filter(Email.content.ilike(f"%{params['content']}%"))
    if params.get("from_time"):
        query = query.filter(Email.email_datetime >= params["from_time"])
    if params.get("to_time"):
        query = query.filter(Email.email_datetime <= params["to_time"])

    return query.order_by(Email.email_datetime.desc()).all()

def search_by_verdict(db: Session, verdict_id: int):
    query = db.query(Email).join(Analysis, Analysis.email_id == Email.id).filter(
        and_(Analysis.verdict_id == verdict_id)
    )
    return query.order_by(Email.email_datetime.desc()).all()


def search_emails_by_text(db: Session, text: str):
    query = db.query(Email).filter(
        or_(
            Email.sender.ilike(f"%{text}%"),
            Email.receiver.ilike(f"%{text}%"),
            Email.content.ilike(f"%{text}%")
        )
    )
    return query.order_by(Email.email_datetime.desc()).all()