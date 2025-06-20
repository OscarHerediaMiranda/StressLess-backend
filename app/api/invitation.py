from datetime import date, datetime
from typing import List
from pydantic import BaseModel
from sqlmodel import Session, select
from app.auth.jwt import verify_token
from app.database.database import get_session
from app.models.models import Colaborador, Invitacion, Lider, LiderColaborador, PreColaborador
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from email_utils import enviar_correo
from datetime import datetime
import random
import string

router = APIRouter()

def generar_otp(longitud=6):
    return ''.join(random.choices(string.digits, k=longitud))

@router.post("/send-invitations/{id_lider}")
def send_invitations(id_lider: int, session: Session = Depends(get_session), token = Depends(verify_token)):
    # 1. Buscar al líder
    lider = session.exec(select(Lider).where(Lider.id == id_lider)).first()
    if not lider:
        raise HTTPException(status_code=404, detail="Líder no encontrado")

    # 2. Buscar los precolaboradores que coinciden con el correo del líder
    precolabs = session.exec(
        select(PreColaborador).where(PreColaborador.correo_lider == lider.correo)
    ).all()

    if not precolabs:
        raise HTTPException(status_code=404, detail="No hay precolaboradores para este líder")

    enviados = []

    for precolab in precolabs:
        # Crear la invitación
        otp = generar_otp()
        invitacion = Invitacion(
            id_precolaborador=precolab.id,
            fecha_envio=date.today(),
            fecha_respuesta=date.today(),
            estado=False,
            codigo=otp,
        )
        session.add(invitacion)
        session.commit()
        session.refresh(invitacion)

        # Crear la relación en tabla intermedia
        relacion = LiderColaborador(
            id_lider=id_lider,
            id_colaborador=None,  # se llenará cuando el colaborador se registre
            estado="pendiente",
            id_invitacion=invitacion.id,
            fecha_inicio=date.today(),
            fecha_fin=date.today()
        )
        session.add(relacion)

        enviar_correo(precolab.correo,otp)

        enviados.append({
            "nombre": precolab.nombre,
            "correo": precolab.correo,
            "codigo": otp

        })

    session.commit()
    return {"mensaje": "Invitaciones enviadas", "invitaciones": enviados}

@router.get("/precolaboradores/{correo_lider}")
def obtener_precolaboradores(correo_lider: str, session: Session = Depends(get_session)):
    precolabs = session.exec(
        select(PreColaborador).where(PreColaborador.correo_lider == correo_lider)
    ).all()
    return precolabs