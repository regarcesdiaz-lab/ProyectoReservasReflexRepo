"""
Estado del formulario de reservas.
Requiere usuario autenticado; precarga sus datos.
"""
from datetime import datetime
import reflex as rx
from ..models.oferta import Oferta
from ..models.reserva import Reserva
from ..models.usuario import Usuario
from .auth_state import AuthState


class ReservasState(rx.State):
    """Estado del formulario de reservas."""

    # Oferta seleccionada
    oferta_id: int = 0
    oferta_titulo: str = ""
    oferta_destino: str = ""
    oferta_precio: float = 0.0
    oferta_duracion: int = 0
    oferta_cargada: bool = False

    # Datos de contacto (se precargan del usuario)
    nombre: str = ""
    apellido: str = ""
    email: str = ""
    telefono: str = ""

    # Detalles de la actividad
    cantidad_personas: int = 1
    fecha_viaje: str = ""
    notas: str = ""

    # Pago
    metodo_pago: str = "tarjeta"

    # Resultado
    mensaje: str = ""
    exito: bool = False
    procesando: bool = False

    @rx.var
    def monto_total(self) -> float:
        return round(self.oferta_precio * self.cantidad_personas, 2)

    @rx.event
    async def cargar_oferta(self):
        """Carga la oferta de ?oferta=ID y precarga datos del usuario logueado."""
        # Verificar autenticación
        auth = await self.get_state(AuthState)
        if not auth.autenticado:
            return rx.redirect("/login")

        # Precargar datos del usuario
        self.nombre = auth.nombre
        self.apellido = auth.apellido
        self.email = auth.email
        # Buscar teléfono en la BD
        with rx.session() as session:
            usuario = session.get(Usuario, auth.usuario_id)
            if usuario:
                self.telefono = usuario.telefono

        # Cargar oferta
        params = self.router.page.params
        id_str = params.get("oferta", "0")
        try:
            self.oferta_id = int(id_str)
        except (ValueError, TypeError):
            return

        with rx.session() as session:
            oferta = session.get(Oferta, self.oferta_id)
            if oferta is None:
                self.mensaje = "Oferta no encontrada."
                return
            self.oferta_titulo = oferta.titulo
            self.oferta_destino = oferta.destino
            self.oferta_precio = oferta.precio
            self.oferta_duracion = oferta.duracion_dias
            self.oferta_cargada = True

    # Setters
    @rx.event
    def set_nombre(self, v: str): self.nombre = v
    @rx.event
    def set_apellido(self, v: str): self.apellido = v
    @rx.event
    def set_email(self, v: str): self.email = v
    @rx.event
    def set_telefono(self, v: str): self.telefono = v
    @rx.event
    def set_cantidad(self, v: str):
        try:
            self.cantidad_personas = max(1, int(v))
        except (ValueError, TypeError):
            self.cantidad_personas = 1
    @rx.event
    def set_fecha_viaje(self, v: str): self.fecha_viaje = v
    @rx.event
    def set_notas(self, v: str): self.notas = v
    @rx.event
    def set_metodo_pago(self, v: str): self.metodo_pago = v

    @rx.event
    async def enviar_reserva(self):
        """Valida y guarda la reserva en MySQL."""
        self.mensaje = ""
        self.exito = False

        auth = await self.get_state(AuthState)
        if not auth.autenticado:
            return rx.redirect("/login")

        if not self.oferta_cargada:
            self.mensaje = "Debes seleccionar una oferta válida."
            return
        if not self.nombre.strip() or not self.apellido.strip():
            self.mensaje = "Nombre y apellido son obligatorios."
            return
        if "@" not in self.email or "." not in self.email:
            self.mensaje = "Correo electrónico inválido."
            return
        if not self.telefono.strip():
            self.mensaje = "Teléfono obligatorio."
            return
        if not self.fecha_viaje:
            self.mensaje = "Selecciona la fecha del viaje."
            return

        self.procesando = True
        try:
            with rx.session() as session:
                nueva = Reserva(
                    oferta_id=self.oferta_id,
                    usuario_id=auth.usuario_id,
                    nombre=self.nombre.strip(),
                    apellido=self.apellido.strip(),
                    email=self.email.strip().lower(),
                    telefono=self.telefono.strip(),
                    cantidad_personas=self.cantidad_personas,
                    fecha_viaje=datetime.fromisoformat(self.fecha_viaje),
                    metodo_pago=self.metodo_pago,
                    notas=self.notas.strip() or None,
                    monto_total=self.monto_total,
                )
                session.add(nueva)
                session.commit()
                session.refresh(nueva)
                self.exito = True
                self.mensaje = (
                    f"¡Reserva #{nueva.id} creada con éxito! "
                    f"Monto total: US${self.monto_total:.2f}. "
                    "Estado: pendiente de confirmación."
                )
                # Limpiar campos editables
                self.cantidad_personas = 1
                self.fecha_viaje = ""
                self.notas = ""
        except Exception as e:
            self.mensaje = f"Error al guardar: {e}"
        finally:
            self.procesando = False
