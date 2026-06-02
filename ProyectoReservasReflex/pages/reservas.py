"""
Página de Reservas (/reservas).
Requiere usuario autenticado.
"""
import reflex as rx
from ..states.reservas_state import ReservasState
from ..components.navbar import navbar
from ..components.footer import footer


def seccion_resumen_oferta() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Oferta seleccionada", size="5"),
            rx.cond(
                ReservasState.oferta_cargada,
                rx.vstack(
                    rx.hstack(
                        rx.icon("plane", size=20, color="#0ea5e9"),
                        rx.text(ReservasState.oferta_titulo, weight="bold", size="4"),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.icon("map-pin", size=16),
                        rx.text(ReservasState.oferta_destino),
                        spacing="1",
                        color="gray",
                    ),
                    rx.hstack(
                        rx.icon("calendar", size=16),
                        rx.text(ReservasState.oferta_duracion, " días"),
                        spacing="1",
                        color="gray",
                    ),
                    rx.text("Precio: US$ ", ReservasState.oferta_precio,
                            " por persona", weight="medium"),
                    spacing="1",
                    align="start",
                ),
                rx.text(
                    "Cargando oferta... Si no aparece, vuelve al inicio y elige una.",
                    color="gray",
                ),
            ),
            spacing="3",
            align="start",
        ),
        padding="1.5em",
        width="100%",
    )


def seccion_datos_contacto() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon("user", size=22, color="#0ea5e9"),
                rx.heading("1. Datos de contacto", size="5"),
                spacing="2",
            ),
            rx.callout(
                "Tus datos se precargaron automáticamente. Edita si necesitas.",
                icon="info", color_scheme="blue", size="1",
            ),
            rx.grid(
                rx.vstack(
                    rx.text("Nombre *", weight="medium", size="2"),
                    rx.input(
                        placeholder="Tu nombre",
                        on_change=ReservasState.set_nombre,
                        value=ReservasState.nombre,
                        size="3", width="100%",
                    ),
                    spacing="1", align="start", width="100%",
                ),
                rx.vstack(
                    rx.text("Apellido *", weight="medium", size="2"),
                    rx.input(
                        placeholder="Tu apellido",
                        on_change=ReservasState.set_apellido,
                        value=ReservasState.apellido,
                        size="3", width="100%",
                    ),
                    spacing="1", align="start", width="100%",
                ),
                columns=rx.breakpoints(initial="1", sm="2"),
                spacing="3", width="100%",
            ),
            rx.grid(
                rx.vstack(
                    rx.text("Correo electrónico *", weight="medium", size="2"),
                    rx.input(
                        placeholder="tu@email.com",
                        type="email",
                        on_change=ReservasState.set_email,
                        value=ReservasState.email,
                        size="3", width="100%",
                    ),
                    spacing="1", align="start", width="100%",
                ),
                rx.vstack(
                    rx.text("Teléfono *", weight="medium", size="2"),
                    rx.input(
                        placeholder="+1 809 555 0123",
                        on_change=ReservasState.set_telefono,
                        value=ReservasState.telefono,
                        size="3", width="100%",
                    ),
                    spacing="1", align="start", width="100%",
                ),
                columns=rx.breakpoints(initial="1", sm="2"),
                spacing="3", width="100%",
            ),
            spacing="4", width="100%",
        ),
        padding="1.5em", width="100%",
    )


def seccion_detalles_actividad() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon("map", size=22, color="#0ea5e9"),
                rx.heading("2. Detalles de la actividad", size="5"),
                spacing="2",
            ),
            rx.grid(
                rx.vstack(
                    rx.text("Cantidad de personas *", weight="medium", size="2"),
                    rx.input(
                        type="number", min="1", max="20",
                        on_change=ReservasState.set_cantidad,
                        value=ReservasState.cantidad_personas.to_string(),
                        size="3", width="100%",
                    ),
                    spacing="1", align="start", width="100%",
                ),
                rx.vstack(
                    rx.text("Fecha del viaje *", weight="medium", size="2"),
                    rx.input(
                        type="date",
                        on_change=ReservasState.set_fecha_viaje,
                        value=ReservasState.fecha_viaje,
                        size="3", width="100%",
                    ),
                    spacing="1", align="start", width="100%",
                ),
                columns=rx.breakpoints(initial="1", sm="2"),
                spacing="3", width="100%",
            ),
            rx.vstack(
                rx.text("Notas adicionales (opcional)", weight="medium", size="2"),
                rx.text_area(
                    placeholder="Restricciones alimentarias, preferencias, etc.",
                    on_change=ReservasState.set_notas,
                    value=ReservasState.notas,
                    size="3", width="100%", rows="3",
                ),
                spacing="1", align="start", width="100%",
            ),
            spacing="4", width="100%",
        ),
        padding="1.5em", width="100%",
    )


def seccion_pago() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon("credit-card", size=22, color="#0ea5e9"),
                rx.heading("3. Descripción de pago", size="5"),
                spacing="2",
            ),
            rx.vstack(
                rx.text("Método de pago *", weight="medium", size="2"),
                rx.radio(
                    ["tarjeta", "transferencia", "efectivo"],
                    on_change=ReservasState.set_metodo_pago,
                    value=ReservasState.metodo_pago,
                    direction="column", spacing="2",
                ),
                spacing="2", align="start", width="100%",
            ),
            rx.divider(),
            rx.vstack(
                rx.hstack(
                    rx.text("Precio por persona:"),
                    rx.spacer(),
                    rx.text("US$ ", ReservasState.oferta_precio),
                    width="100%",
                ),
                rx.hstack(
                    rx.text("Cantidad de personas:"),
                    rx.spacer(),
                    rx.text(ReservasState.cantidad_personas),
                    width="100%",
                ),
                rx.divider(),
                rx.hstack(
                    rx.text("Total a pagar:", weight="bold", size="4"),
                    rx.spacer(),
                    rx.text("US$ ", ReservasState.monto_total,
                            weight="bold", size="6", color="#0ea5e9"),
                    width="100%", align="center",
                ),
                spacing="2", width="100%",
            ),
            rx.callout(
                "El pago se confirma al recibir nuestro correo. Esto es solo un registro de la reserva.",
                icon="info", color_scheme="blue", size="1",
            ),
            spacing="4", width="100%",
        ),
        padding="1.5em", width="100%",
    )


def mensaje_resultado() -> rx.Component:
    return rx.cond(
        ReservasState.mensaje != "",
        rx.callout(
            ReservasState.mensaje,
            icon=rx.cond(ReservasState.exito, "circle-check", "triangle-alert"),
            color_scheme=rx.cond(ReservasState.exito, "green", "red"),
            size="2", width="100%",
        ),
        rx.fragment(),
    )


@rx.page(route="/reservas", title="Reservar - TurismoDO",
         on_load=ReservasState.cargar_oferta)
def reservas() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            rx.vstack(
                rx.heading("Completar reserva", size="8"),
                rx.text("Llena tus datos para confirmar tu próxima aventura", color="gray"),
                seccion_resumen_oferta(),
                seccion_datos_contacto(),
                seccion_detalles_actividad(),
                seccion_pago(),
                mensaje_resultado(),
                rx.button(
                    rx.hstack(
                        rx.icon("send", size=18),
                        rx.text("Confirmar reserva"),
                        spacing="2",
                    ),
                    on_click=ReservasState.enviar_reserva,
                    size="4", background="#0ea5e9", width="100%",
                    loading=ReservasState.procesando,
                    disabled=~ReservasState.oferta_cargada,
                ),
                spacing="4", width="100%", max_width="800px",
            ),
            padding="2em 1.5em",
            display="flex", justify_content="center", width="100%",
        ),
        footer(),
        width="100%", min_height="100vh", background="#f9fafb",
    )
