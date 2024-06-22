from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.enum_verdicts import EnumVerdicts, EnumVerdictsCreate, EnumVerdictsUpdate
from app.crud import enum_verdicts as crud_enum_verdicts
from app.db.database import get_db
from app.api.auth import get_current_user
from app.schemas.user import User

router = APIRouter()

@router.post("/", response_model=EnumVerdicts)
def create_enum_verdicts(enum_verdicts: EnumVerdictsCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_enum_verdicts.create_enum_verdicts(db=db, enum_verdicts=enum_verdicts)

@router.get("/{enum_verdicts_id}", response_model=EnumVerdicts)
def read_enum_verdicts(enum_verdicts_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_enum_verdicts = crud_enum_verdicts.get_enum_verdicts(db, enum_verdicts_id=enum_verdicts_id)
    if db_enum_verdicts is None:
        raise HTTPException(status_code=404, detail="Enum Verdicts not found")
    return db_enum_verdicts

@router.get("/", response_model=List[EnumVerdicts])
def read_enum_verdicts_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    enum_verdicts_all = crud_enum_verdicts.get_enum_verdicts_all(db, skip=skip, limit=limit)
    return enum_verdicts_all

@router.put("/{enum_verdicts_id}", response_model=EnumVerdicts)
def update_enum_verdicts(enum_verdicts_id: int, enum_verdicts: EnumVerdictsUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_enum_verdicts = crud_enum_verdicts.get_enum_verdicts(db, enum_verdicts_id=enum_verdicts_id)
    if db_enum_verdicts is None:
        raise HTTPException(status_code=404, detail="Enum Verdicts not found")
    return crud_enum_verdicts.update_enum_verdicts(db, db_enum_verdicts=db_enum_verdicts, enum_verdicts_update=enum_verdicts)

@router.delete("/{enum_verdicts_id}", response_model=EnumVerdicts)
def delete_enum_verdicts(enum_verdicts_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_enum_verdicts = crud_enum_verdicts.get_enum_verdicts(db, enum_verdicts_id=enum_verdicts_id)
    if db_enum_verdicts is None:
        raise HTTPException(status_code=404, detail="Enum Verdicts not found")
    return crud_enum_verdicts.delete_enum_verdicts(db, enum_verdicts_id=enum_verdicts_id)
