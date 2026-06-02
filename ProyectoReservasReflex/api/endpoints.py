"""
API REST.

Rutas:
  GET  /api/ofertas              -> Listar ofertas activas
  GET  /api/ofertas/{id}         -> Detalle de una oferta
  POST /api/reservas             -> Crear una reserva
  GET  /api/reservas             -> Listar todas las reservas
  GET  /api/sugerencias          -> Listar sugerencias
"""
from datetime import datetime
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr
import reflex as rx

from ..models.oferta import Oferta
from ..models.reserva import Reserva
from ..models.sugerencia import Sugerencia


class ReservaInput(BaseModel):
    oferta_id: int
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str
    cantidad_personas: int
    fecha_viaje: str
    metodo_pago: str
    notas: Optional[str] = None


async def listar_ofertas():
    """GET /api/ofertas"""
    with rx.session() as session:
        ofertas = session.exec(
            Oferta.select().where(Oferta.activa == True)
        ).all()
        return [
            {
                "id": o.id, "titulo": o.titulo, "destino": o.destino,
                "descripcion": o.descripcion, "imagen_url": o.imagen_url,
                "precio": o.precio, "duracion_dias": o.duracion_dias,
            }
            for o in ofertas
        ]


async def obtener_oferta(oferta_id: int):
    """GET /api/ofertas/{oferta_id}"""
    with rx.session() as session:
        oferta = session.get(Oferta, oferta_id)
        if not oferta:
            raise HTTPException(status_code=404, detail="Oferta no encontrada")
        return {
            "id": oferta.id, "titulo": oferta.titulo, "destino": oferta.destino,
            "descripcion": oferta.descripcion,
            "descripcion_larga": oferta.descripcion_larga,
            "imagen_url": oferta.imagen_url, "precio": oferta.precio,
            "duracion_dias": oferta.duracion_dias,
            "itinerario": oferta.itinerario, "incluye": oferta.incluye,
            "activa": oferta.activa,
        }


async def crear_reserva(data: ReservaInput):
    """POST /api/reservas"""
    if data.metodo_pago not in ["tarjeta", "transferencia", "efectivo"]:
        raise HTTPException(status_code=400, detail="Método de pago inválido")
    if data.cantidad_personas < 1:
        raise HTTPException(status_code=400, detail="Cantidad de personas inválida")

    try:
        fecha = datetime.fromisoformat(data.fecha_viaje)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido (YYYY-MM-DD)")

    with rx.session() as session:
        oferta = session.get(Oferta, data.oferta_id)
        if not oferta:
            raise HTTPException(status_code=404, detail="Oferta no encontrada")

        monto = round(oferta.precio * data.cantidad_personas, 2)
        reserva = Reserva(
            oferta_id=data.oferta_id,
            nombre=data.nombre.strip(), apellido=data.apellido.strip(),
            email=str(data.email).lower(), telefono=data.telefono.strip(),
            cantidad_personas=data.cantidad_personas,
            fecha_viaje=fecha, metodo_pago=data.metodo_pago,
            notas=data.notas, monto_total=monto,
        )
        session.add(reserva)
        session.commit()
        session.refresh(reserva)
        return {
            "ok": True, "reserva_id": reserva.id,
            "monto_total": monto, "estado": reserva.estado,
            "mensaje": "Reserva creada con éxito.",
        }


async def listar_reservas():
    """GET /api/reservas"""
    with rx.session() as session:
        reservas = session.exec(Reserva.select()).all()
        return [
            {
                "id": r.id, "oferta_id": r.oferta_id,
                "nombre": r.nombre, "apellido": r.apellido,
                "email": r.email, "telefono": r.telefono,
                "cantidad_personas": r.cantidad_personas,
                "fecha_viaje": r.fecha_viaje.isoformat(),
                "metodo_pago": r.metodo_pago, "estado": r.estado,
                "monto_total": r.monto_total,
                "creada_en": r.creada_en.isoformat(),
            }
            for r in reservas
        ]


async def listar_sugerencias():
    """GET /api/sugerencias"""
    with rx.session() as session:
        sugs = session.exec(Sugerencia.select()).all()
        return [
            {
                "id": s.id, "nombre": s.nombre, "email": s.email,
                "asunto": s.asunto, "mensaje": s.mensaje,
                "leida": s.leida, "creada_en": s.creada_en.isoformat(),
            }
            for s in sugs
        ]
