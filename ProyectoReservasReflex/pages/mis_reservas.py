"""
Página Mis Reservas (/mis-reservas).
El cliente ve sus reservas con estado.
"""
import reflex as rx
from ..states.mis_reservas_state import MisReservasState, MiReservaView
from ..components.navbar import navbar
from ..components.footer import footer


def color_estado(estado: str) -> str:
    return rx.match(
        estado,
        ("pendiente", "yellow"),
        ("confirmada", "green"),
        ("cancelada", "red"),
        "gray",
    )


def tarjeta_reserva(r: MiReservaView) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.heading(r.oferta_titulo, size="4"),
                        rx.badge(r.estado, color_scheme=color_estado(r.estado), size="2"),
                        spacing="2",
                        align="center",
                    ),
                    rx.hstack(
                        rx.icon("map-pin", size=14),
                        rx.text(r.destino, color="gray", size="2"),
                        spacing="1",
                    ),
                    spacing="2",
                    align="start",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.text("Total", color="gray", size="1"),
                    rx.text("US$ ", r.monto_total, weight="bold", size="5",
                            color="#0ea5e9"),
                    spacing="0",
                    align="end",
                ),
                width="100%",
                align="start",
            ),
            rx.divider(),
            rx.grid(
                rx.vstack(
                    rx.text("Reserva #", color="gray", size="1"),
                    rx.text(r.id, weight="medium"),
                    spacing="0", align="start",
                ),
                rx.vstack(
                    rx.text("Fecha viaje", color="gray", size="1"),
                    rx.text(r.fecha_viaje, weight="medium"),
                    spacing="0", align="start",
                ),
                rx.vstack(
                    rx.text("Personas", color="gray", size="1"),
                    rx.text(r.cantidad_personas, weight="medium"),
                    spacing="0", align="start",
                ),
                rx.vstack(
                    rx.text("Pago", color="gray", size="1"),
                    rx.text(r.metodo_pago, weight="medium"),
                    spacing="0", align="start",
                ),
                columns=rx.breakpoints(initial="2", sm="4"),
                spacing="3",
                width="100%",
            ),
            rx.text("Creada: " + r.creada_en, color="gray", size="1"),
            spacing="3",
            width="100%",
        ),
        padding="1.5em",
        width="100%",
    )


@rx.page(route="/mis-reservas", title="Mis Reservas - TurismoDO",
         on_load=MisReservasState.cargar)
def mis_reservas() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            rx.vstack(
                rx.heading("Mis reservas", size="8"),
                rx.text("Historial de tus reservas y su estado actual", color="gray"),
                rx.cond(
                    MisReservasState.cargando,
                    rx.center(rx.spinner(size="3"), padding_y="3em"),
                    rx.cond(
                        MisReservasState.mis_reservas.length() > 0,
                        rx.vstack(
                            rx.foreach(MisReservasState.mis_reservas, tarjeta_reserva),
                            spacing="3",
                            width="100%",
                        ),
                        rx.center(
                            rx.vstack(
                                rx.icon("ticket", size=48, color="gray"),
                                rx.text("Aún no tienes reservas.", color="gray"),
                                rx.link(rx.button("Ver ofertas", background="#0ea5e9"), href="/"),
                                spacing="3",
                                align="center",
                            ),
                            padding_y="3em",
                        ),
                    ),
                ),
                spacing="4",
                width="100%",
                max_width="900px",
            ),
            padding="2em 1.5em",
            display="flex",
            justify_content="center",
            width="100%",
        ),
        footer(),
        width="100%",
        min_height="100vh",
        background="#f9fafb",
    )
