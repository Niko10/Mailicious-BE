from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.alert import Alert, AlertCreate, AlertUpdate
from app.crud import alert as crud_alert
from app.db.database import get_db
from app.api.auth import get_current_user
from app.schemas.user import User

router = APIRouter()

@router.post("/", response_model=Alert)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_alert.create_alert(db=db, alert=alert)

@router.get("/{alert_id}", response_model=Alert)
def read_alert(alert_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_alert = crud_alert.get_alert(db, alert_id=alert_id)
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return db_alert

@router.get("/", response_model=List[Alert])
def read_alerts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alerts = crud_alert.get_alerts(db, skip=skip, limit=limit)
    return alerts

@router.put("/{alert_id}", response_model=Alert)
def update_alert(alert_id: int, alert: AlertUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_alert = crud_alert.get_alert(db, alert_id=alert_id)
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return crud_alert.update_alert(db, db_alert=db_alert, alert_update=alert)

@router.delete("/{alert_id}", response_model=Alert)
def delete_alert(alert_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_alert = crud_alert.get_alert(db, alert_id=alert_id)
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return crud_alert.delete_alert(db, alert_id=alert_id)
