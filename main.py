from fastapi import FastAPI
from auth import router as auth_router
from leader import router as leader_router
from database import create_tables

app = FastAPI()

app.include_router(auth_router)
app.include_router(leader_router)

@app.on_event("startup")
def on_startup():
    create_tables()