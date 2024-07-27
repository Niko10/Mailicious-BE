# app/crud/actions.py
from sqlalchemy.orm import Session
from app.models.actions import Actions 
from app.schemas.actions import ActionRead, ActionBase
from typing import List

def get_actions(db: Session):
    return db.query(Actions).all()

def create_action(db: Session, action: ActionBase):
    db_action = Actions(**action.dict())
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action

def update_actions_bulk(db: Session, actions: List[ActionRead]):
    for action in actions:
        db_action = db.query(Actions).filter(Actions.id == action.id).first()
        for var, value in vars(action).items():
            setattr(db_action, var, value) if value else None
    db.commit()
    return db.query(Actions).all()

def update_action(db: Session, db_action: Actions, action: ActionBase):
    for var, value in vars(action).items():
        setattr(db_action, var, value) if value else None
    db.commit()
    db.refresh(db_action)
    return db_action

