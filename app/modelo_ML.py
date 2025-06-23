from typing import Optional
from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
from sqlalchemy import desc

from sqlmodel import Session, select
from app.database.database import get_session
from datetime import datetime
import shutil
import os
import uuid  

from app.predictor import predecir_estres
from app.models.models import Colaborador, Lider, LiderColaborador, NotificacionLider, ResultadoAnalisis

router = APIRouter()

@router.post("/predecir/")
async def predecir_audio(
    id_colaborador: int = Form(...),
    audio: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    print("🟢 ID recibido:", id_colaborador)
    print("🟢 Archivo recibido:", audio.filename)

    try:
        # Asegurar carpeta
        os.makedirs("audios", exist_ok=True)

        # Crear nombre único
        filename = f"{uuid.uuid4()}.wav"
        file_path = os.path.join("audios", filename)

        # Guardar archivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        # Predecir
        resultado = predecir_estres(file_path)

        # Guardar en tabla PRUEBA
        from app.models.models import Prueba
        nueva_prueba = Prueba(
            id_colaborador=id_colaborador,
            fecha=datetime.utcnow().date(),
            archivo_audio=filename
        )
        #session.add(nueva_prueba)
        #session.commit()
        #session.refresh(nueva_prueba)

        # Guardar en tabla RESULTADO_ANALISIS
        nuevo_resultado = ResultadoAnalisis(
            id_colaborador=id_colaborador,
            id_prueba=nueva_prueba.id,
            resultado=resultado,
            fecha=datetime.utcnow(),
            archivo_audio=filename
        )
        session.add(nuevo_resultado)
        session.commit()

        # LÓGICA PARA LOS 3 ÚLTIMOS RESULTADOS

        contador_resultados = 0
        if resultado == 1:
            
            consulta_estres = select(Prueba.resultado).order_by(Prueba.desc().limit(2))
            resultados = session.exec(consulta_estres).all()

            for resultado in resultados:
                if resultado == 1:
                    contador_resultados += 1

            consulta_colaborador = select(Colaborador).where(Colaborador.id == nuevo_resultado.id_colaborador)
            colaborador:Optional[Colaborador]=session.exec(consulta_colaborador).first()
            nombre_colaborador = colaborador.nombre

            consulta_lider = select(LiderColaborador).where(LiderColaborador.id_colaborador == colaborador.id)
            liderColaborador:Optional[LiderColaborador] = session.exec(consulta_lider).first()

            registro_notificacion = NotificacionLider(
                descripcion = "Tu colaborador {nombre_colaborador} estuvo estresado por 3 días consecutivos. Sugerencia: Conversa con él !!!",
                leido=None,
                id_lider=liderColaborador.id_lider
            )

            session.add(registro_notificacion)
            session.commit()
            session.refresh(registro_notificacion)

        return {
            "resultado": resultado,
            "fecha": nuevo_resultado.fecha.strftime("%Y-%m-%d %H:%M"),
            "archivo": filename
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en predicción: {str(e)}")