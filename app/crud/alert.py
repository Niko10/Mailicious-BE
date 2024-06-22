from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertUpdate
from app.crud.email import create_email, update_email

def get_alert(db: Session, alert_id: int):
    return db.query(Alert).filter(Alert.id == alert_id).first()

def get_alerts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Alert).offset(skip).limit(limit).all()

def create_alert(db: Session, alert: AlertCreate):
    email_data = alert.email
    db_email = create_email(db, email_data)
    db_alert = Alert(rule_name=alert.rule_name, alert_datetime=alert.alert_datetime, email_id=db_email.id, handled=alert.handled, active=alert.active)
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def update_alert(db: Session, db_alert: Alert, alert_update: AlertUpdate):
    if alert_update.email:
        db_email = update_email(db, db_alert.email, alert_update.email)
        db_alert.email_id = db_email.id
    for var, value in vars(alert_update).items():
        if var != 'email':
            setattr(db_alert, var, value) if value else None
    db.commit()
    db.refresh(db_alert)
    return db_alert

def delete_alert(db: Session, alert_id: int):
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    db.delete(db_alert)
    db.commit()
    return db_alert
