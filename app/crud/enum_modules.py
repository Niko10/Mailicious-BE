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

def update_enum_module(db: Session, enum_module: EnumModulesUpdate):
    current_module = db.query(EnumModules).filter(EnumModules.id == enum_module.id).first()
    if not current_module:
        return None
    
    for var, value in vars(enum_module).items():
        if var != "id" and value is not None:
            setattr(current_module, var, value)
    
    db.commit()
    db.refresh(current_module)
    
    return current_module

def delete_enum_modules(db: Session, enum_modules_id: int):
    db_enum_modules = db.query(EnumModules).filter(EnumModules.id == enum_modules_id).first()
    db.delete(db_enum_modules)
    db.commit()
    return db_enum_modules
