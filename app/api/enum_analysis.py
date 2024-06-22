from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.enum_analysis import EnumAnalysis, EnumAnalysisCreate, EnumAnalysisUpdate
from app.crud import enum_analysis as crud_enum_analysis
from app.db.database import get_db
from app.api.auth import get_current_user
from app.schemas.user import User

router = APIRouter()

@router.post("/", response_model=EnumAnalysis)
def create_enum_analysis(enum_analysis: EnumAnalysisCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_enum_analysis.create_enum_analysis(db=db, enum_analysis=enum_analysis)

@router.get("/{enum_analysis_id}", response_model=EnumAnalysis)
def read_enum_analysis(enum_analysis_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_enum_analysis = crud_enum_analysis.get_enum_analysis(db, enum_analysis_id=enum_analysis_id)
    if db_enum_analysis is None:
        raise HTTPException(status_code=404, detail="Enum Analysis not found")
    return db_enum_analysis

@router.get("/", response_model=List[EnumAnalysis])
def read_enum_analyses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    enum_analyses = crud_enum_analysis.get_enum_analyses(db, skip=skip, limit=limit)
    return enum_analyses

@router.put("/{enum_analysis_id}", response_model=EnumAnalysis)
def update_enum_analysis(enum_analysis_id: int, enum_analysis: EnumAnalysisUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_enum_analysis = crud_enum_analysis.get_enum_analysis(db, enum_analysis_id=enum_analysis_id)
    if db_enum_analysis is None:
        raise HTTPException(status_code=404, detail="Enum Analysis not found")
    return crud_enum_analysis.update_enum_analysis(db, db_enum_analysis=db_enum_analysis, enum_analysis_update=enum_analysis)

@router.delete("/{enum_analysis_id}", response_model=EnumAnalysis)
def delete_enum_analysis(enum_analysis_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_enum_analysis = crud_enum_analysis.get_enum_analysis(db, enum_analysis_id=enum_analysis_id)
    if db_enum_analysis is None:
        raise HTTPException(status_code=404, detail="Enum Analysis not found")
    return crud_enum_analysis.delete_enum_analysis(db, enum_analysis_id=enum_analysis_id)
