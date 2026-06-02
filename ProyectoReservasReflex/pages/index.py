"""
Página de Inicio (/).
Hero con búsqueda, ofertas, contacto con formulario de sugerencias.
"""
import reflex as rx
from ..states.ofertas_state import OfertasState
from ..states.sugerencias_state import SugerenciasState
from ..components.navbar import navbar
from ..components.footer import footer
from ..components.oferta_card import oferta_card


def hero_busqueda() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Descubre tu próxima aventura",
                       size="9", color="white", text_align="center"),
            rx.text(
                "Explora los destinos más increíbles de República Dominicana y el mundo",
                color="white", size="4", opacity="0.95",
                text_align="center", max_width="600px",
            ),
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.icon("search", size=20, color="gray"),
                        rx.input(
                            placeholder="¿A dónde quieres ir? (ej. Punta Cana)",
                            on_change=OfertasState.set_destino,
                            value=OfertasState.destino_busqueda,
                            size="3",
                            flex="1",
                        ),
                        width="100%",
                        align="center",
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.icon("calendar", size=20, color="gray"),
                        rx.input(
                            type="date",
                            on_change=OfertasState.set_fecha,
                            value=OfertasState.fecha_busqueda,
                            size="3",
                            flex="1",
                        ),
                        width="100%",
                        align="center",
                        spacing="2",
                    ),
                    rx.button(
                        rx.hstack(rx.icon("search", size=18),
                                  rx.text("Buscar ofertas"), spacing="2"),
                        on_click=OfertasState.buscar,
                        size="3", width="100%", background="#0ea5e9",
                        loading=OfertasState.cargando,
                    ),
                    spacing="3", width="100%",
                ),
                padding="1.5em", width="100%",
                max_width="500px", background="white",
            ),
            spacing="5", align="center",
            padding_y="5em", padding_x="1em",
        ),
        background="linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%)",
        width="100%",
    )


def seccion_ofertas() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Ofertas destacadas", size="8", id="ofertas"),
            rx.text("Las mejores experiencias seleccionadas para ti",
                    color="gray", size="3"),
            rx.cond(
                OfertasState.cargando,
                rx.center(rx.spinner(size="3"), padding_y="3em"),
                rx.cond(
                    OfertasState.ofertas.length() > 0,
                    rx.grid(
                        rx.foreach(OfertasState.ofertas, oferta_card),
                        columns=rx.breakpoints(initial="1", sm="2", md="3"),
                        spacing="4", width="100%",
                    ),
                    rx.center(
                        rx.vstack(
                            rx.icon("search-x", size=40, color="gray"),
                            rx.text("No se encontraron ofertas. Intenta otra búsqueda.",
                                    color="gray"),
                            spacing="2", align="center",
                        ),
                        padding_y="3em",
                    ),
                ),
            ),
            spacing="4", width="100%",
            max_width="1200px", align="center",
        ),
        padding="3em 1.5em", width="100%",
    )


def formulario_sugerencia() -> rx.Component:
    """Formulario de sugerencias/contacto."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon("message-square", size=22, color="#0ea5e9"),
                rx.heading("Envíanos tu sugerencia", size="5"),
                spacing="2",
            ),
            rx.text(
                "¿Tienes una idea, comentario o quieres reportar algo? "
                "Escríbenos, leemos cada mensaje.",
                color="gray", size="2",
            ),
            rx.grid(
                rx.vstack(
                    rx.text("Nombre *", weight="medium", size="2"),
                    rx.input(
                        placeholder="Tu nombre",
                        on_change=SugerenciasState.set_nombre,
                        value=SugerenciasState.nombre,
                        size="3", width="100%",
                    ),
                    spacing="1", align="start", width="100%",
                ),
                rx.vstack(
                    rx.text("Email *", weight="medium", size="2"),
                    rx.input(
                        placeholder="tu@email.com",
                        type="email",
                        on_change=SugerenciasState.set_email,
                        value=SugerenciasState.email,
                        size="3", width="100%",
                    ),
                    spacing="1", align="start", width="100%",
                ),
                columns=rx.breakpoints(initial="1", sm="2"),
                spacing="3", width="100%",
            ),
            rx.vstack(
                rx.text("Asunto *", weight="medium", size="2"),
                rx.input(
                    placeholder="¿Sobre qué nos quieres escribir?",
                    on_change=SugerenciasState.set_asunto,
                    value=SugerenciasState.asunto,
                    size="3", width="100%",
                ),
                spacing="1", align="start", width="100%",
            ),
            rx.vstack(
                rx.text("Mensaje *", weight="medium", size="2"),
                rx.text_area(
                    placeholder="Cuéntanos en detalle...",
                    on_change=SugerenciasState.set_mensaje,
                    value=SugerenciasState.mensaje,
                    size="3", width="100%", rows="5",
                ),
                spacing="1", align="start", width="100%",
            ),
            rx.cond(
                SugerenciasState.resultado != "",
                rx.callout(
                    SugerenciasState.resultado,
                    icon=rx.cond(SugerenciasState.exito, "circle-check", "triangle-alert"),
                    color_scheme=rx.cond(SugerenciasState.exito, "green", "red"),
                    size="1", width="100%",
                ),
                rx.fragment(),
            ),
            rx.button(
                rx.hstack(rx.icon("send", size=18), rx.text("Enviar mensaje"), spacing="2"),
                on_click=SugerenciasState.enviar,
                size="3", width="100%", background="#0ea5e9",
                loading=SugerenciasState.enviando,
            ),
            spacing="3", width="100%",
        ),
        padding="2em", width="100%",
        max_width="700px",
    )


def seccion_contacto() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Contáctanos", size="7", id="contacto"),
            rx.text("Estamos aquí para ayudarte a planificar el viaje perfecto.",
                    color="gray", text_align="center"),
            rx.grid(
                rx.card(
                    rx.vstack(
                        rx.icon("phone", size=28, color="#0ea5e9"),
                        rx.heading("Teléfono", size="4"),
                        rx.text("+1 (809) 555-0123"),
                        spacing="2", align="center",
                    ),
                    padding="1.5em",
                ),
                rx.card(
                    rx.vstack(
                        rx.icon("mail", size=28, color="#0ea5e9"),
                        rx.heading("Email", size="4"),
                        rx.text("info@turismodo.com"),
                        spacing="2", align="center",
                    ),
                    padding="1.5em",
                ),
                rx.card(
                    rx.vstack(
                        rx.icon("map-pin", size=28, color="#0ea5e9"),
                        rx.heading("Dirección", size="4"),
                        rx.text("Av. Winston Churchill", text_align="center"),
                        rx.text("Santo Domingo, R.D.", text_align="center"),
                        spacing="1", align="center",
                    ),
                    padding="1.5em",
                ),
                columns=rx.breakpoints(initial="1", sm="3"),
                spacing="4", width="100%", max_width="900px",
            ),
            formulario_sugerencia(),
            spacing="4", width="100%", align="center",
        ),
        padding="3em 1.5em", width="100%",
        background="#f9fafb",
    )


@rx.page(route="/", title="TurismoDO - Reservas y Ofertas Turísticas",
         on_load=OfertasState.cargar_ofertas)
def index() -> rx.Component:
    return rx.box(
        navbar(),
        hero_busqueda(),
        seccion_ofertas(),
        seccion_contacto(),
        footer(),
        width="100%",
        min_height="100vh",
    )
