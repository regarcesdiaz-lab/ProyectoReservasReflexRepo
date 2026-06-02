"""
Página de Registro (/registro).
"""
import reflex as rx
from ..states.auth_state import AuthState
from ..components.navbar import navbar
from ..components.footer import footer


@rx.page(route="/registro", title="Crear cuenta - TurismoDO")
def registro() -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(
            rx.card(
                rx.vstack(
                    rx.icon("user-plus", size=40, color="#0ea5e9"),
                    rx.heading("Crear cuenta", size="7"),
                    rx.text("Regístrate para empezar a reservar",
                            color="gray", size="2"),
                    rx.divider(),
                    rx.grid(
                        rx.vstack(
                            rx.text("Nombre *", weight="medium", size="2"),
                            rx.input(
                                placeholder="Juan",
                                on_change=AuthState.set_reg_nombre,
                                value=AuthState.reg_nombre,
                                size="3",
                                width="100%",
                            ),
                            spacing="1",
                            align="start",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Apellido *", weight="medium", size="2"),
                            rx.input(
                                placeholder="Pérez",
                                on_change=AuthState.set_reg_apellido,
                                value=AuthState.reg_apellido,
                                size="3",
                                width="100%",
                            ),
                            spacing="1",
                            align="start",
                            width="100%",
                        ),
                        columns=rx.breakpoints(initial="1", sm="2"),
                        spacing="3",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Email *", weight="medium", size="2"),
                        rx.input(
                            placeholder="tu@email.com",
                            type="email",
                            on_change=AuthState.set_reg_email,
                            value=AuthState.reg_email,
                            size="3",
                            width="100%",
                        ),
                        spacing="1",
                        align="start",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Teléfono *", weight="medium", size="2"),
                        rx.input(
                            placeholder="+1 809 555 0123",
                            on_change=AuthState.set_reg_telefono,
                            value=AuthState.reg_telefono,
                            size="3",
                            width="100%",
                        ),
                        spacing="1",
                        align="start",
                        width="100%",
                    ),
                    rx.grid(
                        rx.vstack(
                            rx.text("Contraseña *", weight="medium", size="2"),
                            rx.input(
                                placeholder="Mínimo 6 caracteres",
                                type="password",
                                on_change=AuthState.set_reg_password,
                                value=AuthState.reg_password,
                                size="3",
                                width="100%",
                            ),
                            spacing="1",
                            align="start",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Confirmar *", weight="medium", size="2"),
                            rx.input(
                                placeholder="Repite la contraseña",
                                type="password",
                                on_change=AuthState.set_reg_password2,
                                value=AuthState.reg_password2,
                                size="3",
                                width="100%",
                            ),
                            spacing="1",
                            align="start",
                            width="100%",
                        ),
                        columns=rx.breakpoints(initial="1", sm="2"),
                        spacing="3",
                        width="100%",
                    ),
                    rx.cond(
                        AuthState.reg_error != "",
                        rx.callout(
                            AuthState.reg_error,
                            icon="triangle-alert",
                            color_scheme="red",
                            size="1",
                            width="100%",
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        AuthState.reg_exito != "",
                        rx.callout(
                            AuthState.reg_exito,
                            icon="circle-check",
                            color_scheme="green",
                            size="1",
                            width="100%",
                        ),
                        rx.fragment(),
                    ),
                    rx.button(
                        "Crear cuenta",
                        on_click=AuthState.registrar,
                        size="3",
                        width="100%",
                        background="#0ea5e9",
                        loading=AuthState.procesando,
                    ),
                    rx.hstack(
                        rx.text("¿Ya tienes cuenta?", color="gray", size="2"),
                        rx.link("Inicia sesión", href="/login",
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
                max_width="500px",
            ),
            padding_y="3em",
            padding_x="1em",
            width="100%",
        ),
        footer(),
        width="100%",
        min_height="100vh",
        background="#f9fafb",
    )
