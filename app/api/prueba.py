from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from app.auth.jwt import verify_token
from app.database.database import get_session
from app.models.models import Invitacion, Lider, LiderColaborador, Notificacion, PreColaborador, Prueba

router = APIRouter()

class PruebaRequest(BaseModel):
    id_lider:int
    precollaborators:List[int]

@router.post("/envio-prueba")
def envioPrueba(request:PruebaRequest, session:Session = Depends(get_session), token = Depends(verify_token)):

    pruebasNoEnviadas = []

    for i in request.precollaborators:

        # validar los casos: reenvío de invitación o líder nuevo
        consulta = select(Invitacion).where(Invitacion.id_precolaborador == i)
        invitacion = session.exec(consulta).first()

        # validar si la invitación fue aceptada o no
        if invitacion.estado == True:
            consulta_liderColaborador = select(LiderColaborador).where(LiderColaborador.id_invitacion == invitacion.id)
            liderColaborador = session.exec(consulta_liderColaborador).first()

            prueba:Prueba = Prueba(
                fecha_registro=datetime.now(),
                fecha_resultado=None,
                id_colaborador=liderColaborador.id_colaborador,
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
            
        else:
            consulta_preColaborador = select(PreColaborador).where(PreColaborador.id == i)
            preColaborador = session.exec(consulta_preColaborador).first()

            pruebasNoEnviadas.append(preColaborador)
    
    return pruebasNoEnviadas
        

@router.post("/prueba")
def createPrueba(request:PruebaRequest, session:Session = Depends(get_session), token = Depends(verify_token)):

    for i in request.precollaborators:
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

    # CREAR ENDPOINT QUE LISTE NOTIFICACIONES DE COLABORADOR O LÍDER (POR ID)
    # ENDPOINT QUE BUSQUE LA PRUEBA POR ID.
    return {"prueba":prueba,"notificacion":notificacion}