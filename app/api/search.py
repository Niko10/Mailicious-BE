from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from app.schemas.email import Email, EmailSearchResult, EmailInDBBase
from app.schemas.search import EmailSearchParams, VerdictSearchParams, IntegratedEmailSearchParams, GroupBySearch
from app.crud.search import search_emails, search_by_verdict, search_emails_by_text, create_group_by_search_emails, group_by_options, delete_group_by_search_emails, get_all_group_by_search_emails
from app.db.database import get_db
from app.api.auth import get_current_user
from app.schemas.user import User
import json

DEBUG_MSG_PREFIX = "./app/api/search.py -"

router = APIRouter()

@router.post("/search/email", response_model=List[Email])
def search_email(params: EmailSearchParams, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    results = search_emails(db=db, params=params.dict())
    return results

@router.post("/search/verdict", response_model=List[Email])
def search_verdict(params: VerdictSearchParams, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    results = search_by_verdict(db=db, verdict_id=params.verdict_id, analysis_id=params.analysis_id)
    return results

@router.get("/search/text", response_model=List[Email])
def search_by_text(text: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    results = search_emails_by_text(db=db, text=text)
    return results

@router.get("/search/group/meta")
def group_by(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return group_by_options(db=db)

@router.get("/search/group/delete/{id}", response_model=Any)
def delete_group_by(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print(f"[DEBUG] {DEBUG_MSG_PREFIX} delete_group_by - id: {id}")
    results = delete_group_by_search_emails(db=db, id=id)
    return results

@router.get("/search/group/all", response_model=Any)
def get_all_groups(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print(f"[DEBUG] {DEBUG_MSG_PREFIX} get_all_groups")
    results = get_all_group_by_search_emails(db=db, user_id=current_user.id)
    return results

@router.post("/search/group", response_model=Any)
def group_by(params: GroupBySearch, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    results = create_group_by_search_emails(db=db, params=params.dict(), user_id=current_user.id)
    return results





@router.post("/search/", response_model=List[EmailSearchResult])
def search_advanced(params: IntegratedEmailSearchParams, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    debug_msg_current = f"{DEBUG_MSG_PREFIX} search_advanced"
    print(f"[DEBUG] {debug_msg_current} - Params:\n", params.model_dump())
    results = search_emails(db=db, params=params.model_dump())  
    
    if params.text:
        text_results = search_emails_by_text(db=db, text=params.text)
        results = [email for email in results if email in text_results]

    if params.verdict is not None:
        verdict_results = search_by_verdict(db=db, 
                                            verdict_id=params.verdict.verdict_id, 
                                            analysis_id=params.verdict.analysis_id)
        results = [email for email in results if email in verdict_results]


    # Transform analyses in EmailSearchResult
    transformed_results = []
    for email in results:
        email_dict = email.__dict__
        email_dict['analyses'] = [
            {
                "id": analysis.id,
                "email_id": analysis.email_id,
                "analysis_id": analysis.analysis_id,
                "verdict_id": analysis.verdict_id,
                "analysis": {
                    "id": analysis.analysis.id,
                    "name": analysis.analysis.name,
                    "description": analysis.analysis.description
                },
                "verdict": {
                    "id": analysis.verdict.id,
                    "name": analysis.verdict.name,
                    "description": analysis.verdict.description
                }
            }
            for analysis in email.analyses
        ]
        transformed_result = EmailSearchResult(**email.__dict__)
        transformed_results.append(transformed_result)
    
    return transformed_results
