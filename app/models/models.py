from datetime import date
from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional
from app.models.base import Base

class LiderColaborador(SQLModel, table=True):
    _tablename_ = "lidercolaborador"  # nombre de la tabla en minúsculas
    _table_args_ = {"schema": "public"}  # esquema en PostgreSQL
    id_lider:int = Field(foreign_key="lider.id",primary_key=True)
    id_colaborador:int = Field(foreign_key="colaborador.id",primary_key=True)
    estado:str
    id_invitacion:int = Field(foreign_key="invitacion.id")
    fecha_inicio:date
    fecha_fin:date

    lider: Optional["Lider"] = Relationship(back_populates="colaboradores_link")
    colaborador: Optional["Colaborador"] = Relationship(back_populates="lideres_link")
    invitacion: Optional["Invitacion"] = Relationship(back_populates="lider_colaborador_link")

class Lider(SQLModel, table=True):
    _tablename_ = "lider"  # nombre de la tabla en minúsculas
    _table_args_ = {"schema": "public"}  # esquema en PostgreSQL
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    contrasenia: str
    estado: bool

    colaboradores_link: List[LiderColaborador] = Relationship(back_populates="lider")

class Colaborador(SQLModel, table=True):
    _tablename_ = "colaborador"  # nombre de la tabla en minúsculas
    _table_args_ = {"schema": "public"}  # esquema en PostgreSQL
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    contrasenia: str
    estado:bool

    lideres_link: List[LiderColaborador] = Relationship(back_populates="colaborador")

class Invitacion(SQLModel, table=True):
    _tablename_ = "invitacion"  # nombre de la tabla en minúsculas
    _table_args_ = {"schema": "public"}  # esquema en PostgreSQL
    id:Optional[int] = Field(default=None, primary_key=True)
    fecha_envio:date
    fecha_respuesta:date
    estado:bool
    codigo:str
    lider_colaborador_link: List[LiderColaborador] = Relationship(back_populates="invitacion")