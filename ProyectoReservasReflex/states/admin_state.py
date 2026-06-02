"""
Estado del panel de administración.
Gestiona reservas, ofertas y sugerencias.
"""
from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass
import reflex as rx
from ..models.reserva import Reserva
from ..models.oferta import Oferta
from ..models.sugerencia import Sugerencia
from .auth_state import AuthState


@dataclass
class ReservaAdminView:
    id: int
    oferta_titulo: str
    cliente: str
    email: str
    telefono: str
    cantidad_personas: int
    fecha_viaje: str
    metodo_pago: str
    estado: str
    monto_total: float
    creada_en: str
    notas: str


@dataclass
class OfertaAdminView:
    id: int
    titulo: str
    destino: str
    precio: float
    duracion_dias: int
    activa: bool


@dataclass
class SugerenciaView:
    id: int
    nombre: str
    email: str
    asunto: str
    mensaje: str
    leida: bool
    creada_en: str


class AdminState(rx.State):
    """Estado para el panel de administración."""

    # Tab activa
    tab_activa: str = "reservas"

    # Listas
    reservas: List[ReservaAdminView] = []
    ofertas: List[OfertaAdminView] = []
    sugerencias: List[SugerenciaView] = []

    # Filtros de reservas
    filtro_estado: str = "todas"  # todas | pendiente | confirmada | cancelada

    # Diálogos
    mostrar_dialogo_oferta: bool = False
    editando_oferta_id: int = 0  # 0 = crear nueva

    # Formulario de oferta
    of_titulo: str = ""
    of_destino: str = ""
    of_descripcion: str = ""
    of_descripcion_larga: str = ""
    of_imagen_url: str = ""
    of_precio: str = "0"
    of_duracion: str = "1"
    of_itinerario: str = ""
    of_incluye: str = ""
    of_activa: bool = True
    of_error: str = ""

    mensaje_accion: str = ""
    mensaje_tipo: str = "info"  # info | exito | error

    @rx.event
    async def cargar_todo(self):
        """Verifica admin y carga todos los datos."""
        auth = await self.get_state(AuthState)
        if not auth.autenticado or auth.rol != "admin":
            return rx.redirect("/login")

        self.cargar_reservas()
        self.cargar_ofertas()
        self.cargar_sugerencias()

    @rx.event
    def set_tab(self, tab: str):
        self.tab_activa = tab
        self.mensaje_accion = ""

    # === RESERVAS ===

    def cargar_reservas(self):
        with rx.session() as session:
            query = Reserva.select()
            if self.filtro_estado != "todas":
                query = query.where(Reserva.estado == self.filtro_estado)
            reservas_db = session.exec(query).all()

            ofertas_dict = {
                o.id: o.titulo
                for o in session.exec(Oferta.select()).all()
            }

            self.reservas = [
                ReservaAdminView(
                    id=r.id,
                    oferta_titulo=ofertas_dict.get(r.oferta_id, "Oferta eliminada"),
                    cliente=f"{r.nombre} {r.apellido}",
                    email=r.email,
                    telefono=r.telefono,
                    cantidad_personas=r.cantidad_personas,
                    fecha_viaje=r.fecha_viaje.strftime("%Y-%m-%d"),
                    metodo_pago=r.metodo_pago,
                    estado=r.estado,
                    monto_total=r.monto_total,
                    creada_en=r.creada_en.strftime("%Y-%m-%d %H:%M"),
                    notas=r.notas or "",
                )
                for r in sorted(reservas_db, key=lambda x: x.creada_en, reverse=True)
            ]

    @rx.event
    def set_filtro_estado(self, estado: str):
        self.filtro_estado = estado
        self.cargar_reservas()

    @rx.event
    def confirmar_reserva(self, reserva_id: int):
        with rx.session() as session:
            reserva = session.get(Reserva, reserva_id)
            if reserva:
                reserva.estado = "confirmada"
                session.add(reserva)
                session.commit()
                self.mensaje_accion = f"Reserva #{reserva_id} confirmada."
                self.mensaje_tipo = "exito"
        self.cargar_reservas()

    @rx.event
    def cancelar_reserva(self, reserva_id: int):
        with rx.session() as session:
            reserva = session.get(Reserva, reserva_id)
            if reserva:
                reserva.estado = "cancelada"
                session.add(reserva)
                session.commit()
                self.mensaje_accion = f"Reserva #{reserva_id} cancelada."
                self.mensaje_tipo = "info"
        self.cargar_reservas()

    @rx.event
    def eliminar_reserva(self, reserva_id: int):
        with rx.session() as session:
            reserva = session.get(Reserva, reserva_id)
            if reserva:
                session.delete(reserva)
                session.commit()
                self.mensaje_accion = f"Reserva #{reserva_id} eliminada permanentemente."
                self.mensaje_tipo = "error"
        self.cargar_reservas()

    # === OFERTAS ===

    def cargar_ofertas(self):
        with rx.session() as session:
            ofertas_db = session.exec(Oferta.select()).all()
            self.ofertas = [
                OfertaAdminView(
                    id=o.id,
                    titulo=o.titulo,
                    destino=o.destino,
                    precio=o.precio,
                    duracion_dias=o.duracion_dias,
                    activa=o.activa,
                )
                for o in ofertas_db
            ]

    @rx.event
    def abrir_dialogo_nueva_oferta(self):
        self.editando_oferta_id = 0
        self.of_titulo = ""
        self.of_destino = ""
        self.of_descripcion = ""
        self.of_descripcion_larga = ""
        self.of_imagen_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800"
        self.of_precio = "0"
        self.of_duracion = "1"
        self.of_itinerario = ""
        self.of_incluye = ""
        self.of_activa = True
        self.of_error = ""
        self.mostrar_dialogo_oferta = True

    @rx.event
    def abrir_dialogo_editar_oferta(self, oferta_id: int):
        with rx.session() as session:
            oferta = session.get(Oferta, oferta_id)
            if not oferta:
                return
            self.editando_oferta_id = oferta_id
            self.of_titulo = oferta.titulo
            self.of_destino = oferta.destino
            self.of_descripcion = oferta.descripcion
            self.of_descripcion_larga = oferta.descripcion_larga
            self.of_imagen_url = oferta.imagen_url
            self.of_precio = str(oferta.precio)
            self.of_duracion = str(oferta.duracion_dias)
            self.of_itinerario = oferta.itinerario
            self.of_incluye = oferta.incluye
            self.of_activa = oferta.activa
            self.of_error = ""
            self.mostrar_dialogo_oferta = True

    @rx.event
    def cerrar_dialogo_oferta(self):
        self.mostrar_dialogo_oferta = False

    # Setters formulario oferta
    @rx.event
    def set_of_titulo(self, v: str): self.of_titulo = v
    @rx.event
    def set_of_destino(self, v: str): self.of_destino = v
    @rx.event
    def set_of_descripcion(self, v: str): self.of_descripcion = v
    @rx.event
    def set_of_descripcion_larga(self, v: str): self.of_descripcion_larga = v
    @rx.event
    def set_of_imagen_url(self, v: str): self.of_imagen_url = v
    @rx.event
    def set_of_precio(self, v: str): self.of_precio = v
    @rx.event
    def set_of_duracion(self, v: str): self.of_duracion = v
    @rx.event
    def set_of_itinerario(self, v: str): self.of_itinerario = v
    @rx.event
    def set_of_incluye(self, v: str): self.of_incluye = v
    @rx.event
    def toggle_of_activa(self, v: bool): self.of_activa = v

    @rx.event
    def guardar_oferta(self):
        """Crea o actualiza una oferta."""
        self.of_error = ""
        if not self.of_titulo.strip():
            self.of_error = "El título es obligatorio."
            return
        if not self.of_destino.strip():
            self.of_error = "El destino es obligatorio."
            return
        try:
            precio = float(self.of_precio)
            if precio < 0:
                raise ValueError()
        except ValueError:
            self.of_error = "El precio debe ser un número válido."
            return
        try:
            duracion = int(self.of_duracion)
            if duracion < 1:
                raise ValueError()
        except ValueError:
            self.of_error = "La duración debe ser un entero ≥ 1."
            return

        with rx.session() as session:
            if self.editando_oferta_id > 0:
                # Actualizar
                oferta = session.get(Oferta, self.editando_oferta_id)
                if not oferta:
                    self.of_error = "Oferta no encontrada."
                    return
                oferta.titulo = self.of_titulo.strip()
                oferta.destino = self.of_destino.strip()
                oferta.descripcion = self.of_descripcion.strip()
                oferta.descripcion_larga = self.of_descripcion_larga.strip()
                oferta.imagen_url = self.of_imagen_url.strip()
                oferta.precio = precio
                oferta.duracion_dias = duracion
                oferta.itinerario = self.of_itinerario.strip()
                oferta.incluye = self.of_incluye.strip()
                oferta.activa = self.of_activa
                session.add(oferta)
                self.mensaje_accion = f"Oferta #{self.editando_oferta_id} actualizada."
            else:
                # Crear
                nueva = Oferta(
                    titulo=self.of_titulo.strip(),
                    destino=self.of_destino.strip(),
                    descripcion=self.of_descripcion.strip(),
                    descripcion_larga=self.of_descripcion_larga.strip(),
                    imagen_url=self.of_imagen_url.strip(),
                    precio=precio,
                    duracion_dias=duracion,
                    itinerario=self.of_itinerario.strip(),
                    incluye=self.of_incluye.strip(),
                    activa=self.of_activa,
                )
                session.add(nueva)
                session.commit()
                session.refresh(nueva)
                self.mensaje_accion = f"Oferta #{nueva.id} creada."
            session.commit()
        self.mensaje_tipo = "exito"
        self.mostrar_dialogo_oferta = False
        self.cargar_ofertas()

    @rx.event
    def eliminar_oferta(self, oferta_id: int):
        with rx.session() as session:
            oferta = session.get(Oferta, oferta_id)
            if oferta:
                session.delete(oferta)
                session.commit()
                self.mensaje_accion = f"Oferta #{oferta_id} eliminada."
                self.mensaje_tipo = "error"
        self.cargar_ofertas()

    @rx.event
    def toggle_activa_oferta(self, oferta_id: int):
        with rx.session() as session:
            oferta = session.get(Oferta, oferta_id)
            if oferta:
                oferta.activa = not oferta.activa
                session.add(oferta)
                session.commit()
                estado = "activada" if oferta.activa else "desactivada"
                self.mensaje_accion = f"Oferta #{oferta_id} {estado}."
                self.mensaje_tipo = "info"
        self.cargar_ofertas()

    # === SUGERENCIAS ===

    def cargar_sugerencias(self):
        with rx.session() as session:
            sugs = session.exec(Sugerencia.select()).all()
            self.sugerencias = [
                SugerenciaView(
                    id=s.id,
                    nombre=s.nombre,
                    email=s.email,
                    asunto=s.asunto,
                    mensaje=s.mensaje,
                    leida=s.leida,
                    creada_en=s.creada_en.strftime("%Y-%m-%d %H:%M"),
                )
                for s in sorted(sugs, key=lambda x: x.creada_en, reverse=True)
            ]

    @rx.event
    def marcar_sugerencia_leida(self, sug_id: int):
        with rx.session() as session:
            sug = session.get(Sugerencia, sug_id)
            if sug:
                sug.leida = not sug.leida
                session.add(sug)
                session.commit()
        self.cargar_sugerencias()

    @rx.event
    def eliminar_sugerencia(self, sug_id: int):
        with rx.session() as session:
            sug = session.get(Sugerencia, sug_id)
            if sug:
                session.delete(sug)
                session.commit()
                self.mensaje_accion = f"Sugerencia #{sug_id} eliminada."
                self.mensaje_tipo = "error"
        self.cargar_sugerencias()
