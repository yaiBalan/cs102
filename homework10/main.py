import routers.auth
import routers.notes
from fastapi import FastAPI
from modules.db import db

app = FastAPI()


@app.on_event("startup")
def startup():
    db.connect()


@app.on_event("shutdown")
def shutdown():
    if not db.is_closed():
        db.close()


app.include_router(routers.auth.router)
app.include_router(routers.notes.router)
