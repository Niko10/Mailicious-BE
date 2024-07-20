from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.email import AnalysisInDBBase as Analysis, AnalysisCreate, AnalysisUpdate
from app.crud import analysis as crud_analysis
from app.db.database import get_db
from app.api.auth import get_current_user
from app.schemas.user import User

router = APIRouter()

@router.post("/", response_model=Analysis)
def create_analysis(analysis: AnalysisCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_analysis.create_analysis(db=db, analysis=analysis)

@router.get("/{analysis_id}", response_model=Analysis)
def read_analysis(analysis_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_analysis = crud_analysis.get_analysis(db, analysis_id=analysis_id)
    if db_analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return db_analysis

@router.get("/", response_model=List[Analysis])
def read_analyses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    analyses = crud_analysis.get_analyses(db, skip=skip, limit=limit)
    return analyses

@router.put("/{analysis_id}", response_model=Analysis)
def update_analysis(analysis_id: int, analysis: AnalysisUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_analysis = crud_analysis.get_analysis(db, analysis_id=analysis_id)
    if db_analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return crud_analysis.update_analysis(db, db_analysis=db_analysis, analysis_update=analysis)

@router.delete("/{analysis_id}", response_model=Analysis)
def delete_analysis(analysis_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_analysis = crud_analysis.get_analysis(db, analysis_id=analysis_id)
    if db_analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return crud_analysis.delete_analysis(db, analysis_id=analysis_id)
