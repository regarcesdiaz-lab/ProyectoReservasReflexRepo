"""
Página de Descripción (/oferta/[id]).
"""
import reflex as rx
from ..states.oferta_detalle_state import OfertaDetalleState
from ..components.navbar import navbar
from ..components.footer import footer


def encabezado_oferta() -> rx.Component:
    return rx.box(
        rx.image(
            src=OfertaDetalleState.imagen_url,
            width="100%",
            height=["250px", "350px", "450px"],
            object_fit="cover",
        ),
        rx.box(
            rx.vstack(
                rx.heading(OfertaDetalleState.titulo, size="9", color="white"),
                rx.hstack(
                    rx.icon("map-pin", size=20, color="white"),
                    rx.text(OfertaDetalleState.destino, size="5", color="white"),
                    spacing="2",
                ),
                spacing="2",
                align="start",
            ),
            position="absolute",
            bottom="0",
            left="0",
            right="0",
            padding="2em",
            background="linear-gradient(transparent, rgba(0,0,0,0.7))",
        ),
        position="relative",
        width="100%",
    )


def seccion_descripcion() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Descripción general", size="7"),
            rx.text(
                OfertaDetalleState.descripcion_larga,
                size="3",
                line_height="1.7",
                white_space="pre-wrap",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="2em 1.5em",
        max_width="900px",
        margin="0 auto",
        width="100%",
    )


def seccion_detalles() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Detalles", size="7"),
            rx.grid(
                rx.card(
                    rx.vstack(
                        rx.icon("calendar-days", size=28, color="#0ea5e9"),
                        rx.text("Duración", weight="bold"),
                        rx.text(OfertaDetalleState.duracion_dias, " días"),
                        spacing="2",
                        align="center",
                    ),
                    padding="1.5em",
                ),
                rx.card(
                    rx.vstack(
                        rx.icon("dollar-sign", size=28, color="#0ea5e9"),
                        rx.text("Precio por persona", weight="bold"),
                        rx.text("US$ ", OfertaDetalleState.precio),
                        spacing="2",
                        align="center",
                    ),
                    padding="1.5em",
                ),
                rx.card(
                    rx.vstack(
                        rx.icon("circle-check", size=28, color="#0ea5e9"),
                        rx.text("Incluye", weight="bold"),
                        rx.text(OfertaDetalleState.incluye,
                                font_size="0.9em", text_align="center"),
                        spacing="2",
                        align="center",
                    ),
                    padding="1.5em",
                ),
                columns=rx.breakpoints(initial="1", sm="3"),
                spacing="4",
                width="100%",
            ),
            spacing="4",
            width="100%",
        ),
        padding="2em 1.5em",
        max_width="900px",
        margin="0 auto",
        width="100%",
        background="#f9fafb",
        border_radius="12px",
    )


def seccion_itinerario() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Itinerario", size="7"),
            rx.box(
                rx.text(
                    OfertaDetalleState.itinerario,
                    white_space="pre-wrap",
                    line_height="1.8",
                    size="3",
                ),
                padding="1.5em",
                background="white",
                border_radius="12px",
                border="1px solid #e5e7eb",
                width="100%",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="2em 1.5em",
        max_width="900px",
        margin="0 auto",
        width="100%",
    )


def boton_reservar() -> rx.Component:
    return rx.box(
        rx.button(
            rx.hstack(
                rx.icon("ticket", size=20),
                rx.text("Reservar ahora"),
                spacing="2",
            ),
            on_click=OfertaDetalleState.ir_a_reservar,
            size="4",
            background="#0ea5e9",
        ),
        padding="2em 1.5em 3em",
        text_align="center",
        width="100%",
    )


@rx.page(route="/oferta/[id]", title="Detalle de la oferta",
         on_load=OfertaDetalleState.cargar)
def descripcion() -> rx.Component:
    return rx.box(
        navbar(),
        rx.cond(
            OfertaDetalleState.encontrada,
            rx.vstack(
                encabezado_oferta(),
                seccion_descripcion(),
                seccion_detalles(),
                seccion_itinerario(),
                boton_reservar(),
                spacing="0",
                width="100%",
            ),
            rx.center(
                rx.vstack(
                    rx.icon("circle-alert", size=48, color="gray"),
                    rx.heading("Oferta no encontrada", size="6"),
                    rx.link(rx.button("Volver al inicio"), href="/"),
                    spacing="3",
                    align="center",
                ),
                padding_y="5em",
            ),
        ),
        footer(),
        width="100%",
        min_height="100vh",
    )
