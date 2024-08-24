from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: User, user_update: UserUpdate):
    for var, value in vars(user_update).items():
        setattr(db_user, var, value) if value else None
    if user_update.password:
        db_user.hashed_password = get_password_hash(user_update.password)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user

def reset_password(db: Session, user_id: int, new_password: str, old_password: str):
    old_password_hash = get_password_hash(old_password)
    # search for the user by id and password
    db_user = db.query(User).filter(User.id == user_id, User.hashed_password == old_password_hash).first()
    if not db_user:
        print("[DEBUG] User not found")
        return None

    # update the password
    db_user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(db_user)
    return db_user
    