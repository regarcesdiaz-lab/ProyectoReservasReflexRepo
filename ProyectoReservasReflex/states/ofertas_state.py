"""
Estado para listar y buscar ofertas turísticas.
"""
from typing import List
from dataclasses import dataclass
import reflex as rx
from ..models.oferta import Oferta


@dataclass
class OfertaView:
    id: int
    titulo: str
    destino: str
    descripcion: str
    imagen_url: str
    precio: float
    duracion_dias: int


class OfertasState(rx.State):
    ofertas: List[OfertaView] = []
    destino_busqueda: str = ""
    fecha_busqueda: str = ""
    cargando: bool = False

    @rx.event
    def cargar_ofertas(self):
        self.cargando = True
        try:
            with rx.session() as session:
                results = session.exec(
                    Oferta.select().where(Oferta.activa == True)
                ).all()
                self.ofertas = [
                    OfertaView(
                        id=o.id,
                        titulo=o.titulo,
                        destino=o.destino,
                        descripcion=o.descripcion,
                        imagen_url=o.imagen_url,
                        precio=o.precio,
                        duracion_dias=o.duracion_dias,
                    )
                    for o in results
                ]
        finally:
            self.cargando = False

    @rx.event
    def set_destino(self, valor: str):
        self.destino_busqueda = valor

    @rx.event
    def set_fecha(self, valor: str):
        self.fecha_busqueda = valor

    @rx.event
    def buscar(self):
        self.cargando = True
        try:
            with rx.session() as session:
                query = Oferta.select().where(Oferta.activa == True)
                if self.destino_busqueda.strip():
                    patron = f"%{self.destino_busqueda.strip()}%"
                    query = query.where(Oferta.destino.ilike(patron))
                results = session.exec(query).all()
                self.ofertas = [
                    OfertaView(
                        id=o.id,
                        titulo=o.titulo,
                        destino=o.destino,
                        descripcion=o.descripcion,
                        imagen_url=o.imagen_url,
                        precio=o.precio,
                        duracion_dias=o.duracion_dias,
                    )
                    for o in results
                ]
        finally:
            self.cargando = False
