"""
Modelo Oferta: representa una oferta turística publicada.
"""
from typing import Optional
from datetime import datetime
import reflex as rx
import sqlmodel


class Oferta(rx.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    titulo: str
    destino: str
    descripcion: str
    descripcion_larga: str = sqlmodel.Field(sa_column=sqlmodel.Column(sqlmodel.Text))
    imagen_url: str
    precio: float
    duracion_dias: int
    itinerario: str = sqlmodel.Field(sa_column=sqlmodel.Column(sqlmodel.Text))
    incluye: str = sqlmodel.Field(sa_column=sqlmodel.Column(sqlmodel.Text))
    activa: bool = True
    creada_en: datetime = sqlmodel.Field(default_factory=datetime.utcnow)
