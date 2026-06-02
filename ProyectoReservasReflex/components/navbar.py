"""
Barra de navegación. Cambia según si hay usuario logueado y su rol.
"""
import reflex as rx
from ..states.auth_state import AuthState


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.link(
                rx.hstack(
                    rx.icon("plane", size=28, color="white"),
                    rx.heading("TurismoDO", size="6", color="white"),
                    spacing="2",
                    align="center",
                ),
                href="/",
                text_decoration="none",
            ),
            rx.spacer(),
            rx.hstack(
                rx.link("Inicio", href="/", color="white", weight="medium"),
                rx.cond(
                    AuthState.autenticado,
                    rx.cond(
                        AuthState.es_admin,
                        # Menú admin
                        rx.hstack(
                            rx.link("Panel Admin", href="/admin",
                                    color="white", weight="medium"),
                            rx.menu.root(
                                rx.menu.trigger(
                                    rx.button(
                                        rx.hstack(
                                            rx.icon("user", size=16),
                                            rx.text(AuthState.nombre),
                                            rx.icon("chevron-down", size=14),
                                            spacing="1",
                                        ),
                                        variant="ghost",
                                        color="white",
                                    ),
                                ),
                                rx.menu.content(
                                    rx.menu.item(
                                        rx.hstack(rx.icon("log-out", size=14),
                                                  rx.text("Cerrar sesión"),
                                                  spacing="2"),
                                        on_click=AuthState.cerrar_sesion,
                                    ),
                                ),
                            ),
                            spacing="4",
                            align="center",
                        ),
                        # Menú cliente
                        rx.hstack(
                            rx.link("Mis reservas", href="/mis-reservas",
                                    color="white", weight="medium"),
                            rx.menu.root(
                                rx.menu.trigger(
                                    rx.button(
                                        rx.hstack(
                                            rx.icon("user", size=16),
                                            rx.text(AuthState.nombre),
                                            rx.icon("chevron-down", size=14),
                                            spacing="1",
                                        ),
                                        variant="ghost",
                                        color="white",
                                    ),
                                ),
                                rx.menu.content(
                                    rx.menu.item(
                                        rx.hstack(rx.icon("log-out", size=14),
                                                  rx.text("Cerrar sesión"),
                                                  spacing="2"),
                                        on_click=AuthState.cerrar_sesion,
                                    ),
                                ),
                            ),
                            spacing="4",
                            align="center",
                        ),
                    ),
                    # Sin sesión
                    rx.hstack(
                        rx.link(
                            rx.button("Iniciar sesión", variant="ghost", color="white"),
                            href="/login",
                        ),
                        rx.link(
                            rx.button("Registrarse", background="white", color="#0ea5e9"),
                            href="/registro",
                        ),
                        spacing="2",
                    ),
                ),
                spacing="4",
                align="center",
            ),
            width="100%",
            align="center",
            padding_x="2em",
            padding_y="1em",
        ),
        background="linear-gradient(90deg, #0ea5e9 0%, #6366f1 100%)",
        width="100%",
        position="sticky",
        top="0",
        z_index="100",
        box_shadow="0 2px 8px rgba(0,0,0,0.1)",
    )
