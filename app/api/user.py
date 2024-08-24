from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import User, UserCreate, UserUpdate, ResetPassowrd
from app.crud import user as crud_user
from app.db.database import get_db
from app.api.auth import get_current_user

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
    return crud_user.create_user(db=db, user=user)

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