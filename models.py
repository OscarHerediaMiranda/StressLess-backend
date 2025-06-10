from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

# Tabla intermedia
class LiderColaborador(SQLModel, table=True):
    __tablename__ = "lider_colaborador"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_lider: int = Field(foreign_key="lider.id")
    id_colaborador: Optional[int] = Field(default=None, foreign_key="colaborador.id")
    estado: str
    id_invitacion: Optional[int] = Field(default=None, foreign_key="invitacion.id")
    fecha_inicio: date
    fecha_fin: date

    lider: Optional["Lider"] = Relationship(back_populates="colaboradores_link")
    colaborador: Optional["Colaborador"] = Relationship(back_populates="lideres_link")


# Tabla Lider
class Lider(SQLModel, table=True):
    __tablename__ = "lider"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    contrasenia: str
    estado: bool

    colaboradores_link: List[LiderColaborador] = Relationship(back_populates="lider")


# Tabla Colaborador
class Colaborador(SQLModel, table=True):
    __tablename__ = "colaborador"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    contrasenia: str
    estado: bool

    lideres_link: List[LiderColaborador] = Relationship(back_populates="colaborador")


# Tabla Invitación
class Invitacion(SQLModel, table=True):
    __tablename__ = "invitacion"
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_envio: date
    fecha_respuesta: date
    estado: bool
    codigo: str


# Tabla PreColaborador
class PreColaborador(SQLModel, table=True):
    __tablename__ = "precolaborador"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    correo_lider: str


class ResultadoAnalisis(SQLModel, table=True):
    __tablename__ = "resultado_analisis"
    id: Optional[int] = Field(default=None, primary_key=True)
    id_colaborador: int = Field(foreign_key="colaborador.id")
    resultado: str
    fecha: datetime = Field(default_factory=datetime.utcnow)
    archivo_audio: str  


