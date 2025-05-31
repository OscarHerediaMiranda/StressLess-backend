from datetime import datetime
from pydantic import BaseModel
from sqlmodel import Session, select
from app.database.database import get_session
from app.models.models import Colaborador, Invitacion, LiderColaborador
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

class InvitationRequest(BaseModel):
    id_lider:int
    collaborators:int = []

@router.post("/invitation")
def createInvitation(request:InvitationRequest,session:Session = Depends(get_session),token = Depends(get_session)):
    
    invitacion:Invitacion = Invitacion(
        fecha_envio=datetime.now(),
        fecha_respuesta=None,
        estado=True,
        codigo="123456"
    )

    session.add(invitacion)
    session.commit()
    session.refresh(invitacion)

    for i in request.collaborators:
        consulta = select(Colaborador).where(Colaborador.id == i)
        resultado = session.exec(consulta).first()
        item = LiderColaborador(request.id_lider, i,"Pendiente", invitacion.id, datetime.now(), None)
        session.add(item)
        session.commit()
        session.refresh(item)
        print(item)
        print(resultado)

    

    return invitacion