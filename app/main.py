from fastapi import FastAPI
from app.auth.auth import router as auth_router
from app.api.leader import router as leader_router
from app.api.collaborator import router as collaborator_router
from app.api.invitation import router as invitation_router
from app.database.database import create_tables

app = FastAPI()

app.include_router(auth_router)
app.include_router(leader_router)
app.include_router(collaborator_router)
app.include_router(invitation_router)

@app.on_event("startup")
def on_startup():
    create_tables()