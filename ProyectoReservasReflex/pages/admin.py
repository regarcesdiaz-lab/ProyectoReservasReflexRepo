"""
Panel de Administración (/admin).
Tabs: Reservas | Ofertas | Sugerencias
"""
import reflex as rx
from ..states.admin_state import (
    AdminState, ReservaAdminView, OfertaAdminView, SugerenciaView,
)
from ..components.navbar import navbar
from ..components.footer import footer


def color_estado_reserva(estado: str) -> str:
    return rx.match(
        estado,
        ("pendiente", "yellow"),
        ("confirmada", "green"),
        ("cancelada", "red"),
        "gray",
    )


# === TAB RESERVAS ===

def fila_reserva(r: ReservaAdminView) -> rx.Component:
    return rx.table.row(
        rx.table.cell(rx.text("#", r.id, weight="bold")),
        rx.table.cell(r.oferta_titulo),
        rx.table.cell(
            rx.vstack(
                rx.text(r.cliente, weight="medium", size="2"),
                rx.text(r.email, color="gray", size="1"),
                rx.text(r.telefono, color="gray", size="1"),
                spacing="0", align="start",
            )
        ),
        rx.table.cell(r.fecha_viaje),
        rx.table.cell(rx.text(r.cantidad_personas, " pers.")),
        rx.table.cell(rx.text("US$ ", r.monto_total, weight="bold")),
        rx.table.cell(
            rx.badge(r.estado, color_scheme=color_estado_reserva(r.estado))
        ),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    rx.icon("check", size=14),
                    on_click=AdminState.confirmar_reserva(r.id),
                    color_scheme="green", size="1",
                    title="Confirmar",
                ),
                rx.button(
                    rx.icon("x", size=14),
                    on_click=AdminState.cancelar_reserva(r.id),
                    color_scheme="orange", size="1",
                    title="Cancelar",
                ),
                rx.button(
                    rx.icon("trash-2", size=14),
                    on_click=AdminState.eliminar_reserva(r.id),
                    color_scheme="red", size="1", variant="soft",
                    title="Eliminar",
                ),
                spacing="1",
            )
        ),
    )


def tab_reservas() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Gestión de reservas", size="6"),
            rx.spacer(),
            rx.select(
                ["todas", "pendiente", "confirmada", "cancelada"],
                value=AdminState.filtro_estado,
                on_change=AdminState.set_filtro_estado,
                size="2",
            ),
            width="100%",
            align="center",
        ),
        rx.cond(
            AdminState.reservas.length() > 0,
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("ID"),
                            rx.table.column_header_cell("Oferta"),
                            rx.table.column_header_cell("Cliente"),
                            rx.table.column_header_cell("Fecha viaje"),
                            rx.table.column_header_cell("Personas"),
                            rx.table.column_header_cell("Total"),
                            rx.table.column_header_cell("Estado"),
                            rx.table.column_header_cell("Acciones"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(AdminState.reservas, fila_reserva)
                    ),
                    variant="surface",
                ),
                width="100%",
                overflow_x="auto",
            ),
            rx.center(
                rx.text("No hay reservas para mostrar.", color="gray"),
                padding_y="3em",
            ),
        ),
        spacing="3",
        width="100%",
    )


# === TAB OFERTAS ===

def fila_oferta(o: OfertaAdminView) -> rx.Component:
    return rx.table.row(
        rx.table.cell(rx.text("#", o.id, weight="bold")),
        rx.table.cell(o.titulo),
        rx.table.cell(o.destino),
        rx.table.cell(rx.text("US$ ", o.precio)),
        rx.table.cell(rx.text(o.duracion_dias, " días")),
        rx.table.cell(
            rx.badge(
                rx.cond(o.activa, "Activa", "Inactiva"),
                color_scheme=rx.cond(o.activa, "green", "gray"),
            )
        ),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    rx.icon("pencil", size=14),
                    on_click=AdminState.abrir_dialogo_editar_oferta(o.id),
                    color_scheme="blue", size="1",
                    title="Editar",
                ),
                rx.button(
                    rx.icon("eye", size=14),
                    on_click=AdminState.toggle_activa_oferta(o.id),
                    color_scheme="gray", size="1", variant="soft",
                    title="Activar/Desactivar",
                ),
                rx.button(
                    rx.icon("trash-2", size=14),
                    on_click=AdminState.eliminar_oferta(o.id),
                    color_scheme="red", size="1", variant="soft",
                    title="Eliminar",
                ),
                spacing="1",
            )
        ),
    )


def dialogo_oferta() -> rx.Component:
    """Modal para crear/editar oferta."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    AdminState.editando_oferta_id > 0,
                    "Editar oferta",
                    "Crear nueva oferta",
                )
            ),
            rx.dialog.description(
                "Completa todos los campos para publicar una oferta turística.",
                size="2", color="gray",
            ),
            rx.vstack(
                rx.grid(
                    rx.vstack(
                        rx.text("Título *", weight="medium", size="2"),
                        rx.input(
                            placeholder="Ej. Punta Cana 5 días",
                            on_change=AdminState.set_of_titulo,
                            value=AdminState.of_titulo,
                            size="2", width="100%",
                        ),
                        spacing="1", align="start", width="100%",
                    ),
                    rx.vstack(
                        rx.text("Destino *", weight="medium", size="2"),
                        rx.input(
                            placeholder="Ej. Punta Cana",
                            on_change=AdminState.set_of_destino,
                            value=AdminState.of_destino,
                            size="2", width="100%",
                        ),
                        spacing="1", align="start", width="100%",
                    ),
                    columns="2", spacing="3", width="100%",
                ),
                rx.vstack(
                    rx.text("Descripción corta *", weight="medium", size="2"),
                    rx.input(
                        placeholder="Frase atractiva de 1 línea",
                        on_change=AdminState.set_of_descripcion,
                        value=AdminState.of_descripcion,
                        size="2", width="100%",
                    ),
                    spacing="1", align="start", width="100%",
                ),
                rx.vstack(
                    rx.text("Descripción larga *", weight="medium", size="2"),
                    rx.text_area(
                        placeholder="Descripción detallada del paquete",
                        on_change=AdminState.set_of_descripcion_larga,
                        value=AdminState.of_descripcion_larga,
                        size="2", width="100%", rows="4",
                    ),
                    spacing="1", align="start", width="100%",
                ),
                rx.vstack(
                    rx.text("URL de imagen *", weight="medium", size="2"),
                    rx.input(
                        placeholder="https://...",
                        on_change=AdminState.set_of_imagen_url,
                        value=AdminState.of_imagen_url,
                        size="2", width="100%",
                    ),
                    spacing="1", align="start", width="100%",
                ),
                rx.grid(
                    rx.vstack(
                        rx.text("Precio (US$) *", weight="medium", size="2"),
                        rx.input(
                            type="number", step="0.01", min="0",
                            on_change=AdminState.set_of_precio,
                            value=AdminState.of_precio,
                            size="2", width="100%",
                        ),
                        spacing="1", align="start", width="100%",
                    ),
                    rx.vstack(
                        rx.text("Duración (días) *", weight="medium", size="2"),
                        rx.input(
                            type="number", min="1",
                            on_change=AdminState.set_of_duracion,
                            value=AdminState.of_duracion,
                            size="2", width="100%",
                        ),
                        spacing="1", align="start", width="100%",
                    ),
                    columns="2", spacing="3", width="100%",
                ),
                rx.vstack(
                    rx.text("Itinerario *", weight="medium", size="2"),
                    rx.text_area(
                        placeholder="Día 1: ...\nDía 2: ...",
                        on_change=AdminState.set_of_itinerario,
                        value=AdminState.of_itinerario,
                        size="2", width="100%", rows="4",
                    ),
                    spacing="1", align="start", width="100%",
                ),
                rx.vstack(
                    rx.text("Qué incluye *", weight="medium", size="2"),
                    rx.input(
                        placeholder="Vuelo, hotel, comidas...",
                        on_change=AdminState.set_of_incluye,
                        value=AdminState.of_incluye,
                        size="2", width="100%",
                    ),
                    spacing="1", align="start", width="100%",
                ),
                rx.hstack(
                    rx.switch(
                        on_change=AdminState.toggle_of_activa,
                        checked=AdminState.of_activa,
                    ),
                    rx.text("Oferta activa (visible al público)"),
                    spacing="2", align="center",
                ),
                rx.cond(
                    AdminState.of_error != "",
                    rx.callout(
                        AdminState.of_error,
                        icon="triangle-alert", color_scheme="red", size="1",
                        width="100%",
                    ),
                    rx.fragment(),
                ),
                rx.hstack(
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button("Cancelar", variant="soft",
                                  on_click=AdminState.cerrar_dialogo_oferta),
                    ),
                    rx.button(
                        "Guardar",
                        on_click=AdminState.guardar_oferta,
                        background="#0ea5e9",
                    ),
                    spacing="2",
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            max_width="700px",
        ),
        open=AdminState.mostrar_dialogo_oferta,
    )


def tab_ofertas() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Gestión de ofertas", size="6"),
            rx.spacer(),
            rx.button(
                rx.hstack(
                    rx.icon("plus", size=16),
                    rx.text("Nueva oferta"),
                    spacing="1",
                ),
                on_click=AdminState.abrir_dialogo_nueva_oferta,
                background="#0ea5e9",
            ),
            width="100%",
            align="center",
        ),
        rx.cond(
            AdminState.ofertas.length() > 0,
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("ID"),
                            rx.table.column_header_cell("Título"),
                            rx.table.column_header_cell("Destino"),
                            rx.table.column_header_cell("Precio"),
                            rx.table.column_header_cell("Duración"),
                            rx.table.column_header_cell("Estado"),
                            rx.table.column_header_cell("Acciones"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(AdminState.ofertas, fila_oferta)
                    ),
                    variant="surface",
                ),
                width="100%",
                overflow_x="auto",
            ),
            rx.center(
                rx.text("No hay ofertas. Crea la primera con el botón de arriba.",
                        color="gray"),
                padding_y="3em",
            ),
        ),
        dialogo_oferta(),
        spacing="3",
        width="100%",
    )


# === TAB SUGERENCIAS ===

def tarjeta_sugerencia(s: SugerenciaView) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.heading(s.asunto, size="3"),
                        rx.cond(
                            ~s.leida,
                            rx.badge("NUEVA", color_scheme="blue"),
                            rx.fragment(),
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.hstack(
                        rx.icon("user", size=14),
                        rx.text(s.nombre, color="gray", size="2"),
                        rx.text("•", color="gray"),
                        rx.icon("mail", size=14),
                        rx.text(s.email, color="gray", size="2"),
                        spacing="1",
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                rx.text(s.creada_en, color="gray", size="1"),
                width="100%",
                align="start",
            ),
            rx.divider(),
            rx.text(s.mensaje, size="2", white_space="pre-wrap"),
            rx.hstack(
                rx.spacer(),
                rx.button(
                    rx.cond(s.leida, "Marcar no leída", "Marcar leída"),
                    on_click=AdminState.marcar_sugerencia_leida(s.id),
                    size="1", variant="soft",
                ),
                rx.button(
                    rx.hstack(rx.icon("trash-2", size=14), rx.text("Eliminar"), spacing="1"),
                    on_click=AdminState.eliminar_sugerencia(s.id),
                    size="1", variant="soft", color_scheme="red",
                ),
                spacing="2",
                width="100%",
            ),
            spacing="2",
            width="100%",
        ),
        padding="1.5em",
        width="100%",
        background=rx.cond(s.leida, "white", "#eff6ff"),
    )


def tab_sugerencias() -> rx.Component:
    return rx.vstack(
        rx.heading("Sugerencias y mensajes", size="6"),
        rx.cond(
            AdminState.sugerencias.length() > 0,
            rx.vstack(
                rx.foreach(AdminState.sugerencias, tarjeta_sugerencia),
                spacing="3",
                width="100%",
            ),
            rx.center(
                rx.vstack(
                    rx.icon("message-square", size=40, color="gray"),
                    rx.text("Aún no hay sugerencias.", color="gray"),
                    spacing="2",
                    align="center",
                ),
                padding_y="3em",
            ),
        ),
        spacing="3",
        width="100%",
    )


# === ESTADÍSTICAS ===

def stats_cards() -> rx.Component:
    return rx.grid(
        rx.card(
            rx.hstack(
                rx.icon("ticket", size=32, color="#0ea5e9"),
                rx.vstack(
                    rx.text("Reservas totales", color="gray", size="1"),
                    rx.heading(AdminState.reservas.length(), size="7"),
                    spacing="0", align="start",
                ),
                spacing="3",
                align="center",
            ),
            padding="1.5em",
        ),
        rx.card(
            rx.hstack(
                rx.icon("plane", size=32, color="#10b981"),
                rx.vstack(
                    rx.text("Ofertas", color="gray", size="1"),
                    rx.heading(AdminState.ofertas.length(), size="7"),
                    spacing="0", align="start",
                ),
                spacing="3",
                align="center",
            ),
            padding="1.5em",
        ),
        rx.card(
            rx.hstack(
                rx.icon("message-square", size=32, color="#f59e0b"),
                rx.vstack(
                    rx.text("Sugerencias", color="gray", size="1"),
                    rx.heading(AdminState.sugerencias.length(), size="7"),
                    spacing="0", align="start",
                ),
                spacing="3",
                align="center",
            ),
            padding="1.5em",
        ),
        columns=rx.breakpoints(initial="1", sm="3"),
        spacing="3",
        width="100%",
    )


@rx.page(route="/admin", title="Panel Admin - TurismoDO",
         on_load=AdminState.cargar_todo)
def admin() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("settings", size=32, color="#0ea5e9"),
                    rx.heading("Panel de Administración", size="8"),
                    spacing="2",
                    align="center",
                ),
                rx.text("Gestiona reservas, ofertas y sugerencias", color="gray"),
                stats_cards(),
                rx.cond(
                    AdminState.mensaje_accion != "",
                    rx.callout(
                        AdminState.mensaje_accion,
                        icon="info",
                        color_scheme=rx.match(
                            AdminState.mensaje_tipo,
                            ("exito", "green"),
                            ("error", "red"),
                            "blue",
                        ),
                        width="100%",
                    ),
                    rx.fragment(),
                ),
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger(
                            rx.hstack(rx.icon("ticket", size=16),
                                      rx.text("Reservas"), spacing="1"),
                            value="reservas",
                        ),
                        rx.tabs.trigger(
                            rx.hstack(rx.icon("plane", size=16),
                                      rx.text("Ofertas"), spacing="1"),
                            value="ofertas",
                        ),
                        rx.tabs.trigger(
                            rx.hstack(rx.icon("message-square", size=16),
                                      rx.text("Sugerencias"), spacing="1"),
                            value="sugerencias",
                        ),
                    ),
                    rx.tabs.content(tab_reservas(), value="reservas",
                                    padding_y="1.5em"),
                    rx.tabs.content(tab_ofertas(), value="ofertas",
                                    padding_y="1.5em"),
                    rx.tabs.content(tab_sugerencias(), value="sugerencias",
                                    padding_y="1.5em"),
                    default_value="reservas",
                    value=AdminState.tab_activa,
                    on_change=AdminState.set_tab,
                    width="100%",
                ),
                spacing="4",
                width="100%",
                max_width="1200px",
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
