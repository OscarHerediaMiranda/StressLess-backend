from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session
from app.auth.jwt import verify_token
from app.database.database import get_session
from app.models.models import Notificacion, Prueba
from app.models.models import Notificacion, Prueba, ResultadoAnalisis
from sqlmodel import Session, select



router = APIRouter()

class PruebaRequest(BaseModel):
    id_lider:int
    collaborators:List[int]

@router.post("/prueba")
def createPrueba(request:PruebaRequest, session:Session = Depends(get_session), token = Depends(verify_token)):

    for i in request.collaborators:
        prueba:Prueba = Prueba(
            fecha_registro=datetime.now(),
            fecha_resultado=None,
            id_colaborador=i,
            estado=1,
            resultado=True,
        )
        session.add(prueba)
        session.commit()
        session.refresh(prueba)
        
        notificacion:Notificacion = Notificacion(
            descripcion="Notificacion",
            estado="Pendiente",
            fecha_envio=datetime.now(),
            id_prueba=prueba.id,
        )
        session.add(notificacion),
        session.commit()
        session.refresh(notificacion)

    return {"prueba":prueba,"notificacion":notificacion}


@router.get("/historial/{id_colaborador}")
def get_historial(id_colaborador: int, session: Session = Depends(get_session)):
    resultados = session.exec(
        select(ResultadoAnalisis).where(ResultadoAnalisis.id_colaborador == id_colaborador)
    ).all()
    return resultados