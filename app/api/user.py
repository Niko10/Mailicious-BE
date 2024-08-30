from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import User, UserCreate, UserUpdate, ResetPassowrd
from app.crud import user as crud_user
from app.crud import search as crud_search
from app.models.widget import Widget
from app.db.database import get_db
from app.api.auth import get_current_user
import json

router = APIRouter()

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/me/id")
def read_users_me_id(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id}

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud_user.create_user(db=db, user=user)

    # create 2 defaults widgets for the use

    DEFAULT_WIDGETS = [    
        { "sender": None, "recipients": None, "content": ["Test"], "subject": None, "from_time": None, "to_time": None, "text": None, "verdict": None, "block": True, "alert": None, "final_verdict": None, "group_by_fields": "sender", "name": "Suspicous Sender", "type": "bar"},
        { "sender": None, "recipients": None, "content": ["Test"], "subject": None, "from_time": "2024-01-01T00:00", "to_time": None, "text": None, "verdict": None, "block": True, "alert": None, "final_verdict": None, "group_by_fields": "sender", "name": "Blocked mail rate in 2024", "type": "pie"}
    ]

    for params in DEFAULT_WIDGETS:
        new_widget = Widget(
            user_id=new_user.id,
            config=json.dumps(params),
            name=params["name"],
            type=params["type"]
        )
        db.add(new_widget)
        db.commit()
        db.refresh(new_widget)
        print("[DEBUG] create_user - new_widget: ", new_widget.__dict__)
    
    return new_user


@router.get("/delete/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.delete_user(db, user_id=user_id)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.update_user(db, db_user=db_user, user_update=user)


@router.post("/reset")
def reset_pssword(reset_password: ResetPassowrd, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print("[DEBUG] reset_password - old_password: ", reset_password.old_password, " new_password: ", reset_password.new_password, " current_user id: ", current_user.id)
    current_user_id = current_user.id
    db_user = crud_user.get_user(db, user_id=current_user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud_user.reset_password(db, user_id=current_user_id, old_password=reset_password.old_password, new_password=reset_password.new_password)    