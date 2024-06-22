from sqlalchemy.orm import Session
from app.models.enum_verdicts import EnumVerdicts
from app.schemas.enum_verdicts import EnumVerdictsCreate, EnumVerdictsUpdate

def get_enum_verdicts(db: Session, enum_verdicts_id: int):
    return db.query(EnumVerdicts).filter(EnumVerdicts.id == enum_verdicts_id).first()

def get_enum_verdicts_all(db: Session, skip: int = 0, limit: int = 10):
    return db.query(EnumVerdicts).offset(skip).limit(limit).all()

def create_enum_verdicts(db: Session, enum_verdicts: EnumVerdictsCreate):
    db_enum_verdicts = EnumVerdicts(**enum_verdicts.dict())
    db.add(db_enum_verdicts)
    db.commit()
    db.refresh(db_enum_verdicts)
    return db_enum_verdicts

def update_enum_verdicts(db: Session, db_enum_verdicts: EnumVerdicts, enum_verdicts_update: EnumVerdictsUpdate):
    for var, value in vars(enum_verdicts_update).items():
        setattr(db_enum_verdicts, var, value) if value else None
    db.commit()
    db.refresh(db_enum_verdicts)
    return db_enum_verdicts

def delete_enum_verdicts(db: Session, enum_verdicts_id: int):
    db_enum_verdicts = db.query(EnumVerdicts).filter(EnumVerdicts.id == enum_verdicts_id).first()
    db.delete(db_enum_verdicts)
    db.commit()
    return db_enum_verdicts
