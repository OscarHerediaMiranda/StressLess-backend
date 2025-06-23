from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from app.auth.jwt import verify_token
from app.database.database import get_session
from app.models.models import Invitacion, ResultadoAnalisis, LiderColaborador, NotificacionColaborador, PreColaborador, Prueba
from sqlmodel import Session, select

router = APIRouter()

class PruebaRequest(BaseModel):
    id_lider:int
    precollaborators:List[int]

@router.post("/pruebas")
def envioPrueba(request:PruebaRequest, session:Session = Depends(get_session), token = Depends(verify_token)):

    pruebasNoEnviadas = []

    for i in request.precollaborators:

        #VALIDAR LOS CASOS: REENVÍO DE INVITACIÓN O LÍDER NUEVO

        consulta = select(Invitacion).where(Invitacion.id_precolaborador == i)
        invitacion = session.exec(consulta).first()

        # VALIDAR SI LA INVITACIÓN FUE ACEPTADA O NO

        if invitacion.estado == True:
            consulta_liderColaborador = select(LiderColaborador).where(LiderColaborador.id_invitacion == invitacion.id)
            liderColaborador = session.exec(consulta_liderColaborador).first()

            prueba:Prueba = Prueba(
                fecha_registro=datetime.now(),
                fecha_resultado=None,
                id_colaborador=liderColaborador.id_colaborador,
                estado=1,
                resultado=None, 
            )

            session.add(prueba)
            session.commit()
            session.refresh(prueba)

            notificacion:NotificacionColaborador = NotificacionColaborador(
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
        

# @router.post("/prueba")
# def createPrueba(request:PruebaRequest, session:Session = Depends(get_session), token = Depends(verify_token)):

#     for i in request.precollaborators:
#         prueba:Prueba = Prueba(
#             fecha_registro=datetime.now(),
#             fecha_resultado=None,
#             id_colaborador=i,
#             estado=1,
#             resultado=None,
#         )
#         session.add(prueba)
#         session.commit()
#         session.refresh(prueba)
        
#         notificacion:NotificacionColaborador = NotificacionColaborador(
#             descripcion="Tu lider te ha enviado una prueba. Realizala ahora.",
#             estado="Pendiente",
#             fecha_envio=datetime.now(),
#             id_prueba=prueba.id,
#         )
#         session.add(notificacion),
#         session.commit()
#         session.refresh(notificacion)

#     return {"prueba":prueba,"notificacion":notificacion}


@router.get("/historial/{id_colaborador}")
def get_historial(id_colaborador: int, session: Session = Depends(get_session)):
    resultados = session.exec(
        select(ResultadoAnalisis).where(ResultadoAnalisis.id_colaborador == id_colaborador)
    ).all()
    return resultados
