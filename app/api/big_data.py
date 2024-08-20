from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import big_data as crud_big_data
from app.db.database import get_db
from app.api.auth import get_current_user
from app.schemas.user import User

router = APIRouter()

@router.post("/get_sender_day_mails_with_link_reputation", response_model=int)
def get_sender_day_mails_with_link_reputation(request: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_big_data.get_sender_day_mails_with_link_reputation(db,request)

@router.post("/get_sender_day_mails_with_attachment_reputation", response_model=int)
def get_sender_day_mails_with_attachment_reputation(request: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_big_data.get_sender_day_mails_with_attachment_reputation(db, request)

@router.post("/sender_domain_reputation", response_model=int)

def sender_domain_reputation(request: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_big_data.sender_domain_reputation(db, request)
