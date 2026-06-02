"""
Pie de página común.
"""
import reflex as rx


def footer() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("plane", size=20, color="white"),
                rx.heading("TurismoDO", size="4", color="white"),
                spacing="2",
            ),
            rx.text("Plataforma de Reservas y Ofertas Turísticas",
                    color="white", opacity="0.85"),
            rx.text("© 2026 — Proyecto Final de Desarrollo Web",
                    color="white", opacity="0.7", font_size="0.85em"),
            spacing="2",
            align="center",
            padding_y="2em",
        ),
        background="#1f2937",
        width="100%",
        margin_top="3em",
    )
