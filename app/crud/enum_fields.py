from sqlalchemy.orm import Session
from app.models.fields_enum import FieldsEnum
from app.schemas.fields_enum import FieldsEnumCreate

def create_fields_enum(db: Session, fields_enum: FieldsEnumCreate):
    db_fields_enum = FieldsEnum(**fields_enum.dict())
    db.add(db_fields_enum)
    db.commit()
    db.refresh(db_fields_enum)
    return db_fields_enum

def get_fields_enum(db: Session, fields_enum_id: int):
    return db.query(FieldsEnum).filter(FieldsEnum.id == fields_enum_id).first()

def get_fields_enum_by_name(db: Session, name: str):
    return db.query(FieldsEnum).filter(FieldsEnum.name == name).first()

def get_fields_enums(db: Session, skip: int = 0, limit: int = 0):
    return db.query(FieldsEnum).offset(skip).limit(limit).all()