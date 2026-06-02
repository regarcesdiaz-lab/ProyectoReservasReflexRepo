"""
Configuración del proyecto Reflex.
"""
import os
import reflex as rx
from dotenv import load_dotenv

load_dotenv()

config = rx.Config(
    app_name="ProyectoReservasReflex",
    db_url=os.getenv("DATABASE_URL", "sqlite:///reflex.db"),
    api_url=os.getenv("API_URL", "http://localhost:8000"),
    cors_allowed_origins=["*"],
    tailwind=None,
)
