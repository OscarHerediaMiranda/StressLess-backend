from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.models import Colaborador, Lider, LiderColaborador
from app.database.database import get_session
from pydantic import BaseModel
from app.auth.jwt import create_access_token, verify_token
import bcrypt

router = APIRouter()

@router.post("/leaders")
def createLeader(data:Lider, session:Session = Depends(get_session), token = Depends(verify_token)):

    consulta = select(Lider).where(Lider.correo == data.correo)
    resultado = session.exec(consulta).first()

    if resultado:
        raise HTTPException(status_code=401, detail="Lider ya se encuentra registrado")
    
    data.contrasenia = bcrypt.hashpw(data.contrasenia.encode(),bcrypt.gensalt()).decode("utf-8")

    session.add(data)
    session.commit()
    session.refresh(data)

    return data

@router.get("/leaders")
def getLeaders(session: Session = Depends(get_session), token = Depends(verify_token)):

    consulta = select(Lider).where(Lider.estado == True)
    resultado = session.exec(consulta).all()
    
    return resultado

@router.put("/leaders/{leaders_id}")
def update_leader(leaders_id: int, valor: Lider, session: Session = Depends(get_session), token = Depends(verify_token)):

    consulta = select(Lider).where(Lider.id == leaders_id)
    resultado = session.exec(consulta).first()

    if not resultado:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    valor.contrasenia = bcrypt.hashpw(valor.contrasenia.encode(),bcrypt.gensalt()).decode("utf-8")

    datos_dict = valor.dict(exclude_unset=True)

    for key,value in datos_dict.items():
        setattr(resultado,key,value)

    session.add(resultado)
    session.commit()
    session.refresh(resultado)

    return resultado

@router.delete("leaders/{leaders_id}")
def delete_leader(leaders_id: int, session:Session = Depends(get_session), token = Depends(verify_token)):

    consulta = select(Lider).where(Lider.id == leaders_id)
    resultado = session.exec(consulta).first()

    if not resultado:
        raise HTTPException(status_code=401, detail="Lider no encontrado")
    
    resultado.estado = False

    session.add(resultado)
    session.commit()
    session.refresh(resultado)

    return resultado

@router.get("/leaders/{leaders_id}/collaborators")
def getCollaboratorsByLeaderId(leaders_id:int, session:Session = Depends(get_session), token = Depends(verify_token)):

    consulta_lider = select(Lider).where(Lider.id == leaders_id)
    resultado = session.exec(consulta_lider).all()

    if not resultado:
        raise HTTPException(status_code=401, detail="Lider no encontrado")
    
    consulta = select(Colaborador).join(LiderColaborador,LiderColaborador.id_colaborador == Colaborador.id).where(LiderColaborador.id_lider == leaders_id)
    colaboradores = session.exec(consulta).all()
    
    return colaboradores
