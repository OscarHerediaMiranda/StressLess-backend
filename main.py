from fastapi import FastAPI
from auth import router as auth_router
from leader import router as leader_router
from collaborator import router as collaborator_router
from invitation import router as invitation_router
from database import create_tables
from modelo_ML import router as ml_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(leader_router)
app.include_router(collaborator_router)
app.include_router(invitation_router)
app.include_router(ml_router)

@app.on_event("startup")
def on_startup():
    create_tables()