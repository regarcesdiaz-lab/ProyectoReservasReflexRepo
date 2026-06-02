"""
Estado para la página de detalle de una oferta.
"""
import reflex as rx
from ..models.oferta import Oferta


class OfertaDetalleState(rx.State):
    oferta_id: int = 0
    titulo: str = ""
    destino: str = ""
    descripcion: str = ""
    descripcion_larga: str = ""
    imagen_url: str = ""
    precio: float = 0.0
    duracion_dias: int = 0
    itinerario: str = ""
    incluye: str = ""
    encontrada: bool = False

    @rx.event
    def cargar(self):
        params = self.router.page.params
        id_str = params.get("id", "0")
        try:
            self.oferta_id = int(id_str)
        except (ValueError, TypeError):
            self.encontrada = False
            return

        with rx.session() as session:
            oferta = session.get(Oferta, self.oferta_id)
            if oferta is None:
                self.encontrada = False
                return
            self.titulo = oferta.titulo
            self.destino = oferta.destino
            self.descripcion = oferta.descripcion
            self.descripcion_larga = oferta.descripcion_larga
            self.imagen_url = oferta.imagen_url
            self.precio = oferta.precio
            self.duracion_dias = oferta.duracion_dias
            self.itinerario = oferta.itinerario
            self.incluye = oferta.incluye
            self.encontrada = True

    @rx.event
    def ir_a_reservar(self):
        return rx.redirect(f"/reservas?oferta={self.oferta_id}")
