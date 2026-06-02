"""
Aplicación principal de Reflex.
"""
import reflex as rx
from fastapi import FastAPI

# Importar todas las páginas para que Reflex las registre
from .pages import (
    index, descripcion, reservas, login, registro, mis_reservas, admin,
)

# Importar modelos para Alembic
from .models import Usuario, Oferta, Reserva, Sugerencia

# Endpoints REST
from .api.endpoints import (
    listar_ofertas, obtener_oferta, crear_reserva, listar_reservas,
    listar_sugerencias,
)

# Crear instancia FastAPI con los endpoints
fastapi_app = FastAPI(title="API Reservas Turísticas")

fastapi_app.add_api_route("/api/ofertas", listar_ofertas, methods=["GET"], tags=["Ofertas"])
fastapi_app.add_api_route("/api/ofertas/{oferta_id}", obtener_oferta, methods=["GET"], tags=["Ofertas"])
fastapi_app.add_api_route("/api/reservas", crear_reserva, methods=["POST"], tags=["Reservas"])
fastapi_app.add_api_route("/api/reservas", listar_reservas, methods=["GET"], tags=["Reservas"])
fastapi_app.add_api_route("/api/sugerencias", listar_sugerencias, methods=["GET"], tags=["Sugerencias"])

# CSS global para forzar texto oscuro y mejorar contraste en toda la app
CSS_GLOBAL = """
/* Forzar colores oscuros para texto en toda la app */
body, html {
    color: #1f2937 !important;
    background: #ffffff;
}

/* Encabezados con buen contraste */
h1, h2, h3, h4, h5, h6,
.rt-Heading {
    color: #111827 !important;
    font-weight: 600;
}

/* Párrafos y texto normal */
p, span, label, div.rt-Text {
    color: #374151;
}

/* Texto secundario (grises) que sigue siendo legible */
.rt-r-c-gray, [data-accent-color="gray"] {
    color: #6b7280 !important;
}

/* Inputs y textareas con buen contraste */
input, textarea, select {
    color: #111827 !important;
    background-color: #ffffff !important;
}

input::placeholder, textarea::placeholder {
    color: #9ca3af !important;
    opacity: 1;
}

/* Labels de formularios bien legibles */
label, .rt-Text[data-weight="medium"] {
    color: #1f2937 !important;
    font-weight: 500;
}

/* Tarjetas (cards) con borde sutil */
.rt-Card {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
}

/* Tablas con buen contraste */
table, th, td {
    color: #1f2937;
}

th {
    background-color: #f9fafb;
    font-weight: 600;
}

/* Excepción: texto blanco DEBE seguir siendo blanco (navbar, footer, hero) */
[style*="color: white"], [style*="color:#fff"], [style*="color: #fff"] {
    color: white !important;
}

/* Texto explícitamente gris claro en fondos oscuros se mantiene */
[style*="rgba(255"] {
    /* no tocar */
}
"""

# Crear la app Reflex
app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="medium",
        accent_color="sky",
        gray_color="slate",
        scaling="100%",
    ),
    api_transformer=fastapi_app,
    style={
        "font_family": "Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
    },
    stylesheets=[],
    head_components=[
        rx.el.style(CSS_GLOBAL),
    ],
)
