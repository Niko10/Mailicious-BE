from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.models.email import Email
from app.models.analysis import Analysis
from app.schemas.search import GroupBySearch, IntegratedEmailSearchParams
from app.schemas.widget import WidgetFull, WidgetCreate, WidgetUpdate
from app.models.widget import Widget
import json
from sqlalchemy.orm import aliased
from app.models.enum_modules import EnumModules
from app.models.enum_verdicts import EnumVerdicts
from sqlalchemy.orm import aliased


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
    
    if params.get("block") != None:
        print(f"[DEBUG] {debug_msg_current} Block: ", params["block"])
        query = query.filter(Email.block == params["block"])
    
    if params.get("alert") != None:
        print(f"[DEBUG] {debug_msg_current} Alert: ", params["alert"])
        query = query.filter(Email.alert == params["alert"])
    
    if params.get("id"):
        ids = params["id"]
        query = query.filter(Email.id.in_(ids))
    
    if params.get("final_verdict"):
        final_verdicts = params["final_verdict"]
        final_verdict_conditions = []

        print(f"[DEBUG] {debug_msg_current} Final Verdicts: ", final_verdicts)

        # Aliasing the EnumModules and EnumVerdicts tables for clarity in the join
        EnumModulesAlias = aliased(EnumModules)
        EnumVerdictsAlias = aliased(EnumVerdicts)

        # Join Email -> Analysis -> EnumModules and EnumVerdicts
        query = query.join(Analysis, Email.analyses).join(EnumModulesAlias, Analysis.analysis).join(EnumVerdictsAlias, Analysis.verdict)

        # Create a condition for each string in the final_verdicts list
        for verdict in final_verdicts:
            verdict_condition = EnumVerdictsAlias.name.ilike(f"%{verdict.strip()}%")
            final_verdict_conditions.append(verdict_condition)

        # Filter where EnumModules name is "Final Verdict" and one of the final_verdicts matches
        query = query.filter(
            EnumModulesAlias.name == "Final Verdict",
            or_(*final_verdict_conditions)
        )


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
    print(f"---------1) [DEBUG] {debug_msg_current} - Text:", text)
    
    # Basic text search on Email fields
    basic_query = db.query(Email).filter(
        or_(
            Email.sender.ilike(f"%{text}%"),
            Email.recipients.ilike(f"%{text}%"),
            Email.content.ilike(f"%{text}%"),
            Email.subject.ilike(f"%{text}%"),
            Email.attachments.ilike(f"%{text}%"),
            #Email.SPF_IPs.ilike(f"%{text}%"),
            #Email.SPF_status.ilike(f"%{text}%")
        )
    )
    
    # Alias the EnumModules and EnumVerdicts tables for clarity in the join
    EnumModulesAlias = aliased(EnumModules)
    EnumVerdictsAlias = aliased(EnumVerdicts)

    # Search for "Final Verdict" in EnumVerdicts
    final_verdict_query = db.query(Email).join(Analysis, Email.analyses).join(EnumModulesAlias, Analysis.analysis).join(EnumVerdictsAlias, Analysis.verdict).filter(
        EnumModulesAlias.name == "Final Verdict",
        EnumVerdictsAlias.name.ilike(f"%{text}%")
    )
    
    # Combine the two queries using union
    combined_query = basic_query.union(final_verdict_query).order_by(Email.email_datetime.desc())

    print(f"[DEBUG] {debug_msg_current} search_emails_by_text - Query: ", str(combined_query))
    
    results = combined_query.all()
    print(f"---------2) [DEBUG] {debug_msg_current} search_emails_by_text - Results: ", results)
    
    return results


def delete_group_by_search_emails(db: Session, id: int):
    # delete the widget from the widgets table
    print(f"[DEBUG] {DEBUG_MSG_PREFIX} delete_group_by_search_emails - ID: ", id)
    db.query(Widget).filter(Widget.id == id).delete()
    db.commit()
    return {"message": "Widget deleted successfully."}

def get_all_group_by_search_emails(db: Session, user_id: int):
    # get all the widgets for the user
    print(f"[DEBUG] {DEBUG_MSG_PREFIX} get_all_group_by_search_emails - user_id: ", user_id)
    widgets = db.query(Widget).filter(Widget.user_id == user_id).all()
    print(f"[DEBUG] {DEBUG_MSG_PREFIX} get_all_group_by_search_emails - Widgets: ", widgets)

    data = []
    for widget in widgets:
        print(f"[DEBUG] {DEBUG_MSG_PREFIX} get_all_group_by_search_emails - Widget ID: ", widget.id)
        config = json.loads(widget.config)
        print(f"[DEBUG] {DEBUG_MSG_PREFIX} get_all_group_by_search_emails - Config: ", widget.config)
        print(f"[DEBUG] {DEBUG_MSG_PREFIX} get_all_group_by_search_emails - Config 2: ", config)
        result = group_by_search_emails(db=db, params=config)
        print(f"[DEBUG] {DEBUG_MSG_PREFIX} get_all_group_by_search_emails - Result: ", result)
        data.append({
            "id": widget.id,
            "data": group_by_search_emails(db=db, params=config),
            "name": widget.name,
            "type": widget.type
        })
    print(f"[DEBUG] {DEBUG_MSG_PREFIX} get_all_group_by_search_emails - Data: ", data)
    return data

def create_group_by_search_emails(db: Session, params: dict, user_id: int):
    # save the params to the widgets table
    print(f"[DEBUG] {DEBUG_MSG_PREFIX} create_group_by_search_emails - user_id: ", user_id, " Params:\n", params)
    new_widget = Widget(
        user_id=user_id,
        config=json.dumps(params),
        name=params["name"],
        type=params["type"]
    )
    
    db.add(new_widget)
    db.commit()
    db.refresh(new_widget)
    new_widget_id = new_widget.id
    results = {}
    results["data"] = group_by_search_emails(db=db, params=params)
    results["id"] = new_widget_id
    results["name"] = params["name"]
    results["type"] = params["type"]
    return results
    

def group_by_search_emails(db: Session, params: dict):
    # process the params and return data
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
    
    for removed in ['verdict', 'final_verdict', 'text', 'email_id', 'name', 'type']:
        if removed in options:
            options.remove(removed)

    print(f"[DEBUG] {DEBUG_MSG_PREFIX} group_by_options - Columns: ", options)
    return options