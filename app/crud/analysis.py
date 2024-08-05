from sqlalchemy.orm import Session
from app.models.analysis import Analysis
from app.schemas.email import AnalysisCreate, AnalysisUpdate
from app.crud import email 

def get_analysis(db: Session, analysis_id: int):
    return db.query(Analysis).filter(Analysis.id == analysis_id).first()

def get_analyses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Analysis).offset(skip).limit(limit).all()

def create_analysis(db: Session, analysis: AnalysisCreate):
    db_analysis = Analysis(**analysis.dict())
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    email.update_final_verdict(db, db_analysis.email_id)
    
    return db_analysis

def update_analysis(db: Session, db_analysis: Analysis, analysis_update: AnalysisUpdate):
    for var, value in vars(analysis_update).items():
        setattr(db_analysis, var, value) if value else None
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

def delete_analysis(db: Session, analysis_id: int):
    db_analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    db.delete(db_analysis)
    db.commit()
    return db_analysis
