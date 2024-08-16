from fastapi import FastAPI
from app.api import user,big_data, auth, email, enum_modules, enum_verdicts, search, analysis, enum_fields, blacklist, actions
from app.db.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

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