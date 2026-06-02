"""
Estado para el formulario de sugerencias (en la sección Contacto del inicio).
"""
import reflex as rx
from ..models.sugerencia import Sugerencia


class SugerenciasState(rx.State):
    nombre: str = ""
    email: str = ""
    asunto: str = ""
    mensaje: str = ""
    resultado: str = ""
    exito: bool = False
    enviando: bool = False

    @rx.event
    def set_nombre(self, v: str): self.nombre = v
    @rx.event
    def set_email(self, v: str): self.email = v
    @rx.event
    def set_asunto(self, v: str): self.asunto = v
    @rx.event
    def set_mensaje(self, v: str): self.mensaje = v

    @rx.event
    def enviar(self):
        self.resultado = ""
        self.exito = False
        if not self.nombre.strip():
            self.resultado = "El nombre es obligatorio."
            return
        if "@" not in self.email or "." not in self.email:
            self.resultado = "Correo inválido."
            return
        if not self.asunto.strip():
            self.resultado = "El asunto es obligatorio."
            return
        if len(self.mensaje.strip()) < 10:
            self.resultado = "El mensaje debe tener al menos 10 caracteres."
            return

        self.enviando = True
        try:
            with rx.session() as session:
                nueva = Sugerencia(
                    nombre=self.nombre.strip(),
                    email=self.email.strip().lower(),
                    asunto=self.asunto.strip(),
                    mensaje=self.mensaje.strip(),
                )
                session.add(nueva)
                session.commit()
                self.exito = True
                self.resultado = "¡Gracias! Hemos recibido tu mensaje."
                self.nombre = ""
                self.email = ""
                self.asunto = ""
                self.mensaje = ""
        except Exception as e:
            self.resultado = f"Error al enviar: {e}"
        finally:
            self.enviando = False
