# app/api/actions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import actions as crud_actions
from app.db.database import get_db
from app.api.auth import get_current_user
from app.schemas.user import User
from app.schemas.actions import ActionBase, ActionRead

router = APIRouter()

@router.get("/", response_model=List[ActionRead])
def read_actions(db: Session = Depends(get_db)):
    actions = crud_actions.get_actions(db)
    return actions

@router.post("/update", response_model=List[ActionRead])
def update_actions(actions: List[ActionRead], db: Session = Depends(get_db)):
    actions = crud_actions.update_actions_bulk(db, actions)
    return actions

@router.post("/create", response_model=ActionBase)
def create_action(action: ActionBase, db: Session = Depends(get_db)):
    return crud_actions.create_action(db=db, action=action)

