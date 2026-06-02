"""
Modelo Reserva: una reserva hecha por un cliente.
"""
from typing import Optional
from datetime import datetime
import reflex as rx
import sqlmodel


class Reserva(rx.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    oferta_id: int = sqlmodel.Field(foreign_key="oferta.id")
    usuario_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="usuario.id")
    # Datos del cliente (snapshot, por si el usuario los cambia luego)
    nombre: str
    apellido: str
    email: str
    telefono: str
    cantidad_personas: int
    fecha_viaje: datetime
    metodo_pago: str  # tarjeta | transferencia | efectivo
    notas: Optional[str] = sqlmodel.Field(
        default=None, sa_column=sqlmodel.Column(sqlmodel.Text)
    )
    estado: str = "pendiente"  # pendiente | confirmada | cancelada
    monto_total: float
    creada_en: datetime = sqlmodel.Field(default_factory=datetime.utcnow)
