from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import PreColaborador, Invitacion, LiderColaborador, Lider
from jwt import verify_token
from datetime import date
import random

router = APIRouter()

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
        # Generar código de 5 dígitos
        codigo = str(random.randint(10000, 99999))

        # Crear la invitación
        invitacion = Invitacion(
            fecha_envio=date.today(),
            fecha_respuesta=date.today(),
            estado=False,
            codigo=codigo
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

        # Simulación de envío
        print(f"📩 Simulando envío a {precolab.correo} con código: {codigo}")

        enviados.append({
            "nombre": precolab.nombre,
            "correo": precolab.correo,
            "codigo": codigo
        })

    session.commit()
    return {"mensaje": "Invitaciones enviadas", "invitaciones": enviados}


@router.get("/precolaboradores/{correo_lider}")
def obtener_precolaboradores(correo_lider: str, session: Session = Depends(get_session)):
    precolabs = session.exec(
        select(PreColaborador).where(PreColaborador.correo_lider == correo_lider)
    ).all()
    return precolabs
