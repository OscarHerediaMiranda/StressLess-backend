from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Lider
from database import get_session
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    correo: str
    contrasenia: str

@router.post("/login")
def login(data: LoginRequest, session: Session = Depends(get_session)):
    consulta = select(Lider).where(Lider.correo == data.correo)
    resultado = session.exec(consulta).first()

    if not resultado or resultado.contrasenia != data.contrasenia:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    return {"mensaje": f"Bienvenido {resultado.nombre}"}