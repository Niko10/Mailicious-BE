from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.blacklist import create_blacklist_item, get_blacklist, get_blacklists, get_blacklists_grouped, delete_blacklist_item
from app.schemas.blacklist import BlacklistCreate, Blacklist, BlacklistGrouped, BlacklistDelete, BlackListFlat
from app.db.database import get_db
from typing import List

router = APIRouter()


@router.get("/", response_model=List[BlackListFlat])
def read_blacklists(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    blacklists = get_blacklists(db, skip=skip, limit=limit)
    return blacklists

@router.post("/add", response_model=Blacklist)
def create_blacklist(blacklist: BlacklistCreate, db: Session = Depends(get_db)):
    return create_blacklist_item(db=db, blacklist=blacklist)

@router.post("/delete")
def delete_blacklist(blacklist: BlacklistDelete, db: Session = Depends(get_db)):
    return delete_blacklist_item(db=db, blacklist=blacklist)

@router.get("/grouped", response_model=List[BlacklistGrouped])
def read_blacklists_grouped(db: Session = Depends(get_db)):
    return get_blacklists_grouped(db=db)