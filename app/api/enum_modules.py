from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.enum_modules import EnumModules, EnumModulesCreate, EnumModulesUpdate
from app.crud import enum_modules as crud_enum_modules
from app.db.database import get_db
from app.api.auth import get_current_user
from app.schemas.user import User

router = APIRouter()

@router.post("/update/", response_model=EnumModules)
def update_enum_modules(module: EnumModulesUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_enum_modules.update_enum_module(db, module)

@router.post("/", response_model=EnumModules)
def create_enum_modules(enum_modules: EnumModulesCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_enum_modules.create_enum_modules(db=db, enum_modules=enum_modules)

@router.get("/{enum_modules_id}", response_model=EnumModules)
def read_enum_modules(enum_modules_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_enum_modules = crud_enum_modules.get_enum_modules(db, enum_modules_id=enum_modules_id)
    if db_enum_modules is None:
        raise HTTPException(status_code=404, detail="Enum Analysis not found")
    return db_enum_modules

@router.get("/", response_model=List[EnumModules])
def read_enum_analyses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    enum_analyses = crud_enum_modules.get_enum_analyses(db, skip=skip, limit=limit)
    return enum_analyses

@router.delete("/{enum_modules_id}", response_model=EnumModules)
def delete_enum_modules(enum_modules_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_enum_modules = crud_enum_modules.get_enum_modules(db, enum_modules_id=enum_modules_id)
    if db_enum_modules is None:
        raise HTTPException(status_code=404, detail="Enum Analysis not found")
    return crud_enum_modules.delete_enum_modules(db, enum_modules_id=enum_modules_id)
