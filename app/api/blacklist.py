from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.blacklist import create_blacklist_item, get_blacklist, get_blacklists, get_blacklists_grouped
from app.schemas.blacklist import BlacklistCreate, Blacklist, BlacklistGrouped
from app.db.database import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=Blacklist)
def create_blacklist(blacklist: BlacklistCreate, db: Session = Depends(get_db)):
    print("[DEBUG] blacklist item: ", blacklist)
    return create_blacklist_item(db=db, blacklist=blacklist)

@router.get("/grouped", response_model=List[BlacklistGrouped])
def read_blacklists_grouped(db: Session = Depends(get_db)):
    return get_blacklists_grouped(db=db)