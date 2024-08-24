from fastapi import FastAPI, Request
from app.api import user, big_data, auth, email, enum_modules, enum_verdicts, search, analysis, enum_fields, blacklist, actions
from app.db.database import engine, Base, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.email import Email
from app.models.analysis import Analysis

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(auth.router, tags=["auth"])
app.include_router(email.router, prefix="/emails", tags=["emails"])
app.include_router(enum_modules.router, prefix="/enum_modules", tags=["enum_modules"])
app.include_router(enum_verdicts.router, prefix="/enum_verdicts", tags=["enum_verdicts"])
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
app.include_router(search.router, tags=["search"])
app.include_router(enum_fields.router, prefix="/fields_enum", tags=["fields_enum"])
app.include_router(blacklist.router, prefix="/blacklist", tags=["blacklist"])
app.include_router(actions.router, prefix="/actions", tags=["actions"])
app.include_router(big_data.router, tags=["big_data"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

# Middleware to delete emails older than 12 months
@app.middleware("http")
async def delete_old_emails(request: Request, call_next):
    # Calculate the date 12 months ago from now
    twelve_months_ago = datetime.utcnow() - timedelta(days=365)
    print(f"Twelve months ago: {twelve_months_ago}")

    # Create a new database session
    db: Session = SessionLocal()

    try:
        # Get IDs of all Emails with datetime older than 12 months
        emails_to_delete = db.query(Email.id).filter(Email.email_datetime < twelve_months_ago).all()
        print(f"Email_ids to delete: {emails_to_delete}")
    
        # Delete emails older than 12 months
        deleted_emails_count = db.query(Email).filter(Email.email_datetime < twelve_months_ago).delete(synchronize_session=False)
        db.commit()
        print(f"Deleted {deleted_emails_count} emails older than 12 months")

        # convert emails_to_delete to a list of integers
        emails_to_delete = [int(email_id) for email_id, in emails_to_delete]

        # Delete all analysis that email_id is in the list of emails_to_delete
        deleted_analysis_count = db.query(Analysis).filter(Analysis.email_id.in_(emails_to_delete)).delete(synchronize_session=False)
        db.commit()
        print(f"Deleted {deleted_analysis_count} analyses older than 12 months")
    except Exception as e:
        print(f"Error deleting old emails: {e}")
        db.rollback()
    finally:
        db.close()

    # Proceed to the next middleware or request handler
    response = await call_next(request)
    return response
