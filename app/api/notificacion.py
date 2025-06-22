from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.auth.jwt import verify_token
from app.database.database import get_session
from app.models.models import NotificacionColaborador, NotificacionLider, Prueba

router = APIRouter()

class NotificacionRequest(BaseModel):
    id_lider:int
    preCollaborators:List[int]

@router.get("/notificaciones/colaborador/{id_colaborador}")
def notificacionColaborador(id_colaborador:int, session:Session = Depends(get_session), token = Depends(verify_token)):

    consulta = select(NotificacionColaborador).where(NotificacionColaborador.id_colaborador == id_colaborador)
    colaborador = session.exec(consulta).all()

    return colaborador

@router.get("/notificaciones/lider/{id_lider}")
def notificacionLider(id_lider:int, session:Session = Depends(get_session), token = Depends(verify_token)):

    consulta = select(NotificacionLider).where(NotificacionLider.id_lider == id_lider)
    lider = session.exec(consulta).all()

    return lider
    