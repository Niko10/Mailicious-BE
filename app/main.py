from fastapi import FastAPI
from app.api import user, auth
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(auth.router, tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}
