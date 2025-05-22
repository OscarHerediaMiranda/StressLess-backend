from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Lider
from database import get_session
from pydantic import BaseModel
from jwt import create_access_token, verify_token

router = APIRouter()

class LeaderRequest(BaseModel):
    id:int
    nombre:str
    correo:str
    contrasenia:str

@router.get("/leaders")
def getLeaders(session: Session = Depends(get_session), data = Depends(verify_token)):

    consulta = select(Lider).where(Lider.estado == True)
    resultado = session.exec(consulta).all()
    
    return resultado