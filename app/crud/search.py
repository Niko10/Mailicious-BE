from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.models.email import Email
from app.models.analysis import Analysis
from app.schemas.search import GroupBySearch, IntegratedEmailSearchParams
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

def group_by_search_emails(db: Session, params: dict):
    print(f"[DEBUG] {DEBUG_MSG_PREFIX} group_by_search_emails - Params:\n", params)
    debug_msg_current = f"{DEBUG_MSG_PREFIX} group_by_search_emails"

    query = db.query(Email)
    
    first = True
    select_fields_names = []
    # Convert string fields to actual column objects
    for field_name in params["group_by_fields"].split(","):
        print(f"[DEBUG] {debug_msg_current} - Field Name: ", field_name)
        # Use getattr to get the column from the Email model, assuming the field exists
        field = getattr(Email, field_name, None)
        if field is not None:
            if first is True:
                query = query.with_entities(field)
                first = False
            else:
                query = query.add_columns(field)
            select_fields_names.append(field_name)
        else:
            # Raise an error or handle the case where the field does not exist
            raise ValueError(f"Field {field_name} does not exist in the Email model.")
    
    query = query.add_columns(func.count().label('count'))
    print(f"[DEBUG] {debug_msg_current} - Query after adding SELECT: ", str(query))

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
    
    if params.get("block"):
        query = query.filter(Email.block == params["block"])
    
    if params.get("alert"):
        query = query.filter(Email.alert == params["alert"])

    print(f"[DEBUG] {debug_msg_current} - Query after adding WHERE: ", str(query))

    group_by_fields = params.get("group_by_fields")
    for field_name in group_by_fields.split(","):
        field = getattr(Email, field_name, None)
        if field is not None:
            query = query.group_by(field)
        else:
            raise ValueError(f"Field {field_name} does not exist in the Email model.")

    print(f"[DEBUG] {debug_msg_current} - Final Query: ", str(query))
    results = query.all()
    formed_results = {}
    for field_name in select_fields_names:
        formed_results[field_name] = []
    
    formed_results["count"] = []
    select_fields_names.append("count")
    for result in results:
        for j, field_name in enumerate(select_fields_names):
            formed_results[field_name].append(result[j])
        
    print(f"[DEBUG] {debug_msg_current} - Results: ", formed_results)
    return formed_results

def group_by_options(db: Session):
    # Get all the columns in the GroupBySearch
    options = []
    for field in GroupBySearch.__annotations__.keys():
        print(field)
        options.append(field)

    for field in IntegratedEmailSearchParams.__annotations__.keys():
        print(field)
        options.append(field)
    
    for removed in ['verdict', 'final_verdict', 'text']:
        options.remove(removed)
        
    print(f"[DEBUG] {DEBUG_MSG_PREFIX} group_by_options - Columns: ", options)
    return options