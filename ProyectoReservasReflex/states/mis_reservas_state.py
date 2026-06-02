"""
Estado para que un cliente vea sus propias reservas.
"""
from typing import List
from dataclasses import dataclass
import reflex as rx
from ..models.reserva import Reserva
from ..models.oferta import Oferta
from .auth_state import AuthState


@dataclass
class MiReservaView:
    id: int
    oferta_titulo: str
    destino: str
    fecha_viaje: str
    cantidad_personas: int
    estado: str
    monto_total: float
    metodo_pago: str
    creada_en: str


class MisReservasState(rx.State):
    mis_reservas: List[MiReservaView] = []
    cargando: bool = False

    @rx.event
    async def cargar(self):
        auth = await self.get_state(AuthState)
        if not auth.autenticado:
            return rx.redirect("/login")

        self.cargando = True
        try:
            with rx.session() as session:
                reservas_db = session.exec(
                    Reserva.select().where(Reserva.usuario_id == auth.usuario_id)
                ).all()
                ofertas_dict = {
                    o.id: (o.titulo, o.destino)
                    for o in session.exec(Oferta.select()).all()
                }
                self.mis_reservas = [
                    MiReservaView(
                        id=r.id,
                        oferta_titulo=ofertas_dict.get(r.oferta_id, ("?", "?"))[0],
                        destino=ofertas_dict.get(r.oferta_id, ("?", "?"))[1],
                        fecha_viaje=r.fecha_viaje.strftime("%Y-%m-%d"),
                        cantidad_personas=r.cantidad_personas,
                        estado=r.estado,
                        monto_total=r.monto_total,
                        metodo_pago=r.metodo_pago,
                        creada_en=r.creada_en.strftime("%Y-%m-%d %H:%M"),
                    )
                    for r in sorted(reservas_db, key=lambda x: x.creada_en, reverse=True)
                ]
        finally:
            self.cargando = False
