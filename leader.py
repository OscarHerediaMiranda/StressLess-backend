from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Lider
from database import get_session
from pydantic import BaseModel
from jwt import create_access_token, verify_token
import bcrypt

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

@router.put("/leaders/{leaders_id}")
def update_leader(leaders_id: int, valor: Lider, session: Session = Depends(get_session)):

    consulta = select(Lider).where(Lider.id == leaders_id)
    resultado = session.exec(consulta).first()

    if not resultado:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    valor.contrasenia = bcrypt.hashpw(valor.contrasenia.encode("utf-8"),bcrypt.gensalt())

    datos_dict = valor.dict(exclude_unset=True)

    for key,value in datos_dict.items():
        setattr(resultado,key,value)

    session.add(resultado)
    session.commit()
    session.refresh(resultado)

    return resultado