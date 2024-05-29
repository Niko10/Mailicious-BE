from fastapi import FastAPI
from app.api import user
from app.db.database import engine
from app.models import user as user_model

user_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}
