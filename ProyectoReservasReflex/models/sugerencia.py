"""
Modelo Sugerencia: comentarios/sugerencias enviados por los usuarios.
"""
from typing import Optional
from datetime import datetime
import reflex as rx
import sqlmodel


class Sugerencia(rx.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    nombre: str
    email: str
    asunto: str
    mensaje: str = sqlmodel.Field(sa_column=sqlmodel.Column(sqlmodel.Text))
    leida: bool = False
    creada_en: datetime = sqlmodel.Field(default_factory=datetime.utcnow)
