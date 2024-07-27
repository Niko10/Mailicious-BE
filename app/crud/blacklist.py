from sqlalchemy.orm import Session
from app.models.blacklist import Blacklist
from app.schemas.blacklist import BlacklistCreate, BlacklistGrouped, BlacklistDelete
from sqlalchemy import func
from app.models.fields_enum import FieldsEnum

def create_blacklist_item(db: Session, blacklist: BlacklistCreate):
    db_blacklist = Blacklist(**blacklist.dict())
    db.add(db_blacklist)
    db.commit()
    db.refresh(db_blacklist)
    return db_blacklist

def delete_blacklist_item(db: Session, blacklist: BlacklistDelete):
    db_blacklist = db.query(Blacklist).filter(Blacklist.id == blacklist.id).first()
    
    if db_blacklist:
        db.delete(db_blacklist)
        db.commit()
        return True
    return False
        

def get_blacklist(db: Session, blacklist_id: int):
    return db.query(Blacklist).filter(Blacklist.id == blacklist_id).first()

def get_blacklists(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Blacklist).offset(skip).limit(limit).all()

def get_blacklists_grouped(db: Session):
    results = db.query(
        Blacklist.field_id,
        FieldsEnum.name.label('field_name'),
        func.group_concat(Blacklist.value).label('values')
    ).join(FieldsEnum).group_by(Blacklist.field_id).all()
    
    return [BlacklistGrouped(field_id=r.field_id, field_name=r.field_name, values=r.values) for r in results]