from fastapi import FastAPI
from app.api import user, auth, email, enum_analysis, enum_verdicts, analysis, search
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(auth.router, tags=["auth"])
app.include_router(email.router, prefix="/emails", tags=["emails"])
app.include_router(enum_analysis.router, prefix="/enum_analysis", tags=["enum_analysis"])
app.include_router(enum_verdicts.router, prefix="/enum_verdicts", tags=["enum_verdicts"])
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
app.include_router(search.router, tags=["search"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}