from sqlalchemy.orm import Session
from app.models.enum_analysis import EnumAnalysis
from app.schemas.enum_analysis import EnumAnalysisCreate, EnumAnalysisUpdate

def get_enum_analysis(db: Session, enum_analysis_id: int):
    return db.query(EnumAnalysis).filter(EnumAnalysis.id == enum_analysis_id).first()

def get_enum_analyses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(EnumAnalysis).offset(skip).limit(limit).all()

def create_enum_analysis(db: Session, enum_analysis: EnumAnalysisCreate):
    db_enum_analysis = EnumAnalysis(**enum_analysis.dict())
    db.add(db_enum_analysis)
    db.commit()
    db.refresh(db_enum_analysis)
    return db_enum_analysis

def update_enum_analysis(db: Session, db_enum_analysis: EnumAnalysis, enum_analysis_update: EnumAnalysisUpdate):
    for var, value in vars(enum_analysis_update).items():
        setattr(db_enum_analysis, var, value) if value else None
    db.commit()
    db.refresh(db_enum_analysis)
    return db_enum_analysis

def delete_enum_analysis(db: Session, enum_analysis_id: int):
    db_enum_analysis = db.query(EnumAnalysis).filter(EnumAnalysis.id == enum_analysis_id).first()
    db.delete(db_enum_analysis)
    db.commit()
    return db_enum_analysis
