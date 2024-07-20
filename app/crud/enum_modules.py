from sqlalchemy.orm import Session
from app.models.enum_modules import EnumModules
from app.schemas.enum_modules import EnumModulesCreate, EnumModulesUpdate

def get_enum_modules(db: Session, enum_modules_id: int):
    return db.query(EnumModules).filter(EnumModules.id == enum_modules_id).first()

def get_enum_analyses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(EnumModules).offset(skip).limit(limit).all()

def create_enum_modules(db: Session, enum_modules: EnumModulesCreate):
    db_enum_modules = EnumModules(**enum_modules.dict())
    db.add(db_enum_modules)
    db.commit()
    db.refresh(db_enum_modules)
    return db_enum_modules

def update_enum_modules(db: Session, db_enum_modules: EnumModules, enum_modules_update: EnumModulesUpdate):
    for var, value in vars(enum_modules_update).items():
        setattr(db_enum_modules, var, value) if value else None
    db.commit()
    db.refresh(db_enum_modules)
    return db_enum_modules

def delete_enum_modules(db: Session, enum_modules_id: int):
    db_enum_modules = db.query(EnumModules).filter(EnumModules.id == enum_modules_id).first()
    db.delete(db_enum_modules)
    db.commit()
    return db_enum_modules
