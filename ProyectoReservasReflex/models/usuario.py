"""
Modelo Usuario: usuarios registrados (clientes y administradores).
"""
from typing import Optional
from datetime import datetime
import reflex as rx
import sqlmodel


class Usuario(rx.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    email: str = sqlmodel.Field(unique=True, index=True)
    telefono: str
    password_hash: str  # nunca guardar contraseñas en texto plano
    rol: str = "cliente"  # "admin" o "cliente"
    activo: bool = True
    creado_en: datetime = sqlmodel.Field(default_factory=datetime.utcnow)
