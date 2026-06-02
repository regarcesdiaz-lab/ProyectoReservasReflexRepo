"""
Tarjeta visual de oferta turística.
"""
import reflex as rx
from ..states.ofertas_state import OfertaView


def oferta_card(oferta: OfertaView) -> rx.Component:
    return rx.link(
        rx.card(
            rx.vstack(
                rx.image(
                    src=oferta.imagen_url,
                    width="100%",
                    height="200px",
                    object_fit="cover",
                    border_radius="8px 8px 0 0",
                ),
                rx.vstack(
                    rx.heading(oferta.titulo, size="4"),
                    rx.hstack(
                        rx.icon("map-pin", size=16),
                        rx.text(oferta.destino, weight="medium"),
                        spacing="1",
                        color="#0ea5e9",
                    ),
                    rx.text(oferta.descripcion, font_size="0.9em",
                            color="gray", no_of_lines=2),
                    rx.hstack(
                        rx.badge(
                            rx.hstack(
                                rx.icon("calendar", size=14),
                                rx.text(oferta.duracion_dias, " días"),
                                spacing="1",
                            ),
                            color_scheme="blue",
                        ),
                        rx.spacer(),
                        rx.text("US$", oferta.precio, weight="bold",
                                size="5", color="#0ea5e9"),
                        width="100%",
                        align="center",
                    ),
                    padding="1em",
                    spacing="2",
                    align="start",
                    width="100%",
                ),
                spacing="0",
                width="100%",
            ),
            padding="0",
            overflow="hidden",
            _hover={"transform": "translateY(-4px)", "box_shadow": "lg"},
            transition="all 0.2s ease",
            width="100%",
            cursor="pointer",
        ),
        href=f"/oferta/{oferta.id}",
        text_decoration="none",
        color="inherit",
        width="100%",
    )
