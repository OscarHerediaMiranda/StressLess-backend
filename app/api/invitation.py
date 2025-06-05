from datetime import datetime
from typing import List
from pydantic import BaseModel
from sqlmodel import Session, select
from app.auth.jwt import verify_token
from app.database.database import get_session
from app.models.models import Colaborador, Invitacion, LiderColaborador
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from email_utils import enviar_correo
from datetime import datetime
import random
import string

router = APIRouter()

def generar_otp(longitud=6):
    return ''.join(random.choices(string.digits, k=longitud))

otp = generar_otp()

class InvitationRequest(BaseModel):
    id_lider:int
    collaborators:List[int]

@router.post("/invitation")
def createInvitation(request:InvitationRequest,session:Session = Depends(get_session),token = Depends(verify_token)):
    
    if token["id"] != request.id_lider:
        raise HTTPException(status_code=401, detail="Lider no encontrado")
    
    invitacion:Invitacion = Invitacion(fecha_envio=datetime.now(),fecha_respuesta=None,estado=True,codigo=generar_otp())

    session.add(invitacion)
    session.commit()
    session.refresh(invitacion)

    for i in request.collaborators:
        item = LiderColaborador(
            id_lider=request.id_lider,
            id_colaborador=i,
            estado="Pendiente",
            id_invitacion=invitacion.id,
            fecha_inicio=datetime.now(),
            fecha_fin=None
        )
        session.add(item)
        session.commit()
        session.refresh(item)

        consulta = select(Colaborador).where(Colaborador.id == i)
        colaborador = session.exec(consulta).first()

        enviar_correo(colaborador.correo,otp)

    return token