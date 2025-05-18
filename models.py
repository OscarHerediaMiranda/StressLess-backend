from sqlmodel import SQLModel, Field
from typing import Optional

class Lider(SQLModel, table=True):
    _tablename_ = "lider"  # nombre de la tabla en minúsculas
    _table_args_ = {"schema": "public"}  # esquema en PostgreSQL
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    nombre_lider: str
    contrasenia: str

class Colaborador(SQLModel, table=True):
    _tablename_ = "colaborador"  # nombre de la tabla en minúsculas
    _table_args_ = {"schema": "public"}  # esquema en PostgreSQL
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    nombre_lider: str
    contrasenia: str