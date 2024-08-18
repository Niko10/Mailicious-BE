from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from app.models.email import Email
from app.models.analysis import Analysis
from app.models.actions import Actions
from fastapi import HTTPException
from datetime import datetime, timedelta

def get_sender_day_mails_with_link_reputation(
    db: Session, request: dict
) -> int:
    today = datetime.now().date()
    link_regex = "(https{0,1}\:\/\/\S+|www\.\S+|\S+\.com)[^\w]"

    try:
        if request.get("sender"):
            count_result  = (
                db.query(func.count(distinct(Email.recipients)))
                
                .filter(
                    Email.content.op('REGEXP')(link_regex),  # Use REGEXP for regex matching
                    Email.sender == request["sender"],
                    func.date(Email.email_datetime) >= today
                )
                .scalar()
            )

            return count_result 
        else:
            raise Exception("sender field is not in the request")


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_sender_day_mails_with_attachment_reputation(
    db: Session,request: dict
) -> int:
    today = datetime.now().date()

    try:
        if request.get("sender"):

            # Query to count distinct receivers for mails with attachments sent today by the specified sender
            count = (
                db.query(func.count(distinct(Email.recipients)))
                .filter(
                    Email.sender == request["sender"],
                    Email.attachments != "",  # Check if attachments array has elements
                    func.date(Email.email_datetime) >= today  # Compare only the date part
                )
                .scalar()
            )
            return count
        else:
            raise Exception("sender field is not in the request")      

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def sender_domain_reputation(
    db: Session, request: dict
) -> int:

    two_weeks_ago = datetime.now().date() - timedelta(weeks=2)

    try:
        if request.get("sender_domain"):
            # Query to count emails from the specified domain in the last two weeks
            count = (
                db.query(func.count(Email.id))
                .filter(
                    Email.sender.like(f"%@{request['sender_domain']}"),  # Match the domain in the sender email
                    func.date(Email.email_datetime) >= two_weeks_ago  # Emails sent in the last two weeks
                )
                .scalar()
            )
            return count
        else:
            raise Exception("sender_domain field is not in the request")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))