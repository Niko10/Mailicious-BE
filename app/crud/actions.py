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
    print("----------------- Debugging -----------------")
    print("actions to update: ")
    for action in actions:
        print(action.__dict__)

    for action in actions:
        db_action = db.query(Actions).filter(Actions.id == action.id).first()
        print("db_action to update: ", db_action.__dict__)
        for var, value in vars(action).items():
            print(f"{var} = {value}")
            setattr(db_action, var, value) if value else None
            
        db.commit()
        print("db_action: ", db_action.__dict__)
        db.refresh(db_action)

    new_actions = db.query(Actions).all()
    print("new_actions: ", new_actions)
    print("----------------- Debugging -----------------")
    return new_actions

def update_action(db: Session, db_action: Actions, action: ActionBase):
    for var, value in vars(action).items():
        setattr(db_action, var, value) if value else None
    db.commit()
    db.refresh(db_action)
    return db_action

