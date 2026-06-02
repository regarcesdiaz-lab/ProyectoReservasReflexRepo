"""
Página de Login (/login).
"""
import reflex as rx
from ..states.auth_state import AuthState
from ..components.navbar import navbar
from ..components.footer import footer


@rx.page(route="/login", title="Iniciar sesión - TurismoDO")
def login() -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(
            rx.card(
                rx.vstack(
                    rx.icon("log-in", size=40, color="#0ea5e9"),
                    rx.heading("Iniciar sesión", size="7"),
                    rx.text("Ingresa con tu cuenta para continuar",
                            color="gray", size="2"),
                    rx.divider(),
                    rx.vstack(
                        rx.text("Email", weight="medium", size="2"),
                        rx.input(
                            placeholder="tu@email.com",
                            type="email",
                            on_change=AuthState.set_login_email,
                            value=AuthState.login_email,
                            size="3",
                            width="100%",
                        ),
                        spacing="1",
                        align="start",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Contraseña", weight="medium", size="2"),
                        rx.input(
                            placeholder="••••••••",
                            type="password",
                            on_change=AuthState.set_login_password,
                            value=AuthState.login_password,
                            size="3",
                            width="100%",
                        ),
                        spacing="1",
                        align="start",
                        width="100%",
                    ),
                    rx.cond(
                        AuthState.login_error != "",
                        rx.callout(
                            AuthState.login_error,
                            icon="triangle-alert",
                            color_scheme="red",
                            size="1",
                            width="100%",
                        ),
                        rx.fragment(),
                    ),
                    rx.button(
                        "Entrar",
                        on_click=AuthState.iniciar_sesion,
                        size="3",
                        width="100%",
                        background="#0ea5e9",
                        loading=AuthState.procesando,
                    ),
                    rx.hstack(
                        rx.text("¿No tienes cuenta?", color="gray", size="2"),
                        rx.link("Regístrate aquí", href="/registro",
                                color="#0ea5e9", weight="medium"),
                        spacing="1",
                        justify="center",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                padding="2em",
                width="100%",
                max_width="400px",
            ),
            padding_y="4em",
            padding_x="1em",
            width="100%",
        ),
        footer(),
        width="100%",
        min_height="100vh",
        background="#f9fafb",
    )
