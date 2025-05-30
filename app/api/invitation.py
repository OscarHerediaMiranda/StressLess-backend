from datetime import datetime
from pydantic import BaseModel
from sqlmodel import Session, select
from app.database.database import get_session
from app.models.models import Invitacion
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

class InvitationRequest(BaseModel):
    id_lider:int
    id_colaborador:str

@router.post("/invitation")
def createInvitation(request:InvitationRequest=[],session:Session = Depends(get_session),token = Depends(get_session)):
    
    invitacion:Invitacion = Invitacion(
        fecha_envio=datetime.now(),
        fecha_respuesta=None,
        estado=True,
        codigo="123456"
    )

    session.add(invitacion)
    session.commit()
    session.refresh(invitacion)

    

    return invitacion