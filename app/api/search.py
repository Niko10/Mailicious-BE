from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.email import Email
from app.schemas.search import EmailSearchParams, VerdictSearchParams, IntegratedEmailSearchParams
from app.crud.search import search_emails, search_by_verdict, search_emails_by_text
from app.db.database import get_db
from app.api.auth import get_current_user
from app.schemas.user import User

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

@router.post("/search/advanced", response_model=List[Email])
def search_advanced(params: IntegratedEmailSearchParams, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    breakpoint()
    results = search_emails(db=db, params=params.dict())
    
    if params.text:
        text_results = search_emails_by_text(db=db, text=params.text)
        # get the commons:
        results = [email for email in results if email in text_results]
    return results

