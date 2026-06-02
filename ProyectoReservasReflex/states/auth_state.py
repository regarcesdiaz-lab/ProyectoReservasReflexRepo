"""
Estado de autenticación global.
Maneja login, registro, logout y sesión.
"""
import reflex as rx
from ..models.usuario import Usuario
from ..utils.auth import hash_password, verify_password


class AuthState(rx.State):
    """Estado global de autenticación."""

    # Datos de sesión
    usuario_id: int = 0
    nombre: str = ""
    apellido: str = ""
    email: str = ""
    rol: str = ""
    autenticado: bool = False

    # Formulario de login
    login_email: str = ""
    login_password: str = ""
    login_error: str = ""

    # Formulario de registro
    reg_nombre: str = ""
    reg_apellido: str = ""
    reg_email: str = ""
    reg_telefono: str = ""
    reg_password: str = ""
    reg_password2: str = ""
    reg_error: str = ""
    reg_exito: str = ""

    procesando: bool = False

    @rx.var
    def es_admin(self) -> bool:
        return self.autenticado and self.rol == "admin"

    @rx.var
    def es_cliente(self) -> bool:
        return self.autenticado and self.rol == "cliente"

    @rx.var
    def nombre_completo(self) -> str:
        if self.autenticado:
            return f"{self.nombre} {self.apellido}"
        return ""

    # Setters login
    @rx.event
    def set_login_email(self, v: str):
        self.login_email = v
        self.login_error = ""
    @rx.event
    def set_login_password(self, v: str):
        self.login_password = v
        self.login_error = ""

    # Setters registro
    @rx.event
    def set_reg_nombre(self, v: str): self.reg_nombre = v
    @rx.event
    def set_reg_apellido(self, v: str): self.reg_apellido = v
    @rx.event
    def set_reg_email(self, v: str): self.reg_email = v
    @rx.event
    def set_reg_telefono(self, v: str): self.reg_telefono = v
    @rx.event
    def set_reg_password(self, v: str): self.reg_password = v
    @rx.event
    def set_reg_password2(self, v: str): self.reg_password2 = v

    @rx.event
    def iniciar_sesion(self):
        """Procesa el login."""
        self.login_error = ""
        if not self.login_email or not self.login_password:
            self.login_error = "Email y contraseña son obligatorios."
            return

        self.procesando = True
        try:
            with rx.session() as session:
                usuario = session.exec(
                    Usuario.select().where(
                        Usuario.email == self.login_email.strip().lower()
                    )
                ).first()

                if not usuario:
                    self.login_error = "Email o contraseña incorrectos."
                    return
                if not usuario.activo:
                    self.login_error = "Tu cuenta está desactivada."
                    return
                if not verify_password(self.login_password, usuario.password_hash):
                    self.login_error = "Email o contraseña incorrectos."
                    return

                # Login exitoso
                self.usuario_id = usuario.id
                self.nombre = usuario.nombre
                self.apellido = usuario.apellido
                self.email = usuario.email
                self.rol = usuario.rol
                self.autenticado = True
                self.login_email = ""
                self.login_password = ""

                # Redirigir según el rol
                if usuario.rol == "admin":
                    return rx.redirect("/admin")
                else:
                    return rx.redirect("/")
        finally:
            self.procesando = False

    @rx.event
    def registrar(self):
        """Procesa el registro de un nuevo usuario."""
        self.reg_error = ""
        self.reg_exito = ""

        # Validaciones
        if not self.reg_nombre.strip() or not self.reg_apellido.strip():
            self.reg_error = "Nombre y apellido son obligatorios."
            return
        if "@" not in self.reg_email or "." not in self.reg_email:
            self.reg_error = "Correo electrónico inválido."
            return
        if not self.reg_telefono.strip():
            self.reg_error = "El teléfono es obligatorio."
            return
        if len(self.reg_password) < 6:
            self.reg_error = "La contraseña debe tener al menos 6 caracteres."
            return
        if self.reg_password != self.reg_password2:
            self.reg_error = "Las contraseñas no coinciden."
            return

        self.procesando = True
        try:
            with rx.session() as session:
                # Verificar que el email no exista
                existe = session.exec(
                    Usuario.select().where(
                        Usuario.email == self.reg_email.strip().lower()
                    )
                ).first()
                if existe:
                    self.reg_error = "Ya existe una cuenta con ese email."
                    return

                nuevo = Usuario(
                    nombre=self.reg_nombre.strip(),
                    apellido=self.reg_apellido.strip(),
                    email=self.reg_email.strip().lower(),
                    telefono=self.reg_telefono.strip(),
                    password_hash=hash_password(self.reg_password),
                    rol="cliente",
                )
                session.add(nuevo)
                session.commit()
                self.reg_exito = "¡Cuenta creada! Ahora puedes iniciar sesión."
                # Limpiar
                self.reg_nombre = ""
                self.reg_apellido = ""
                self.reg_email = ""
                self.reg_telefono = ""
                self.reg_password = ""
                self.reg_password2 = ""
                return rx.redirect("/login")
        except Exception as e:
            self.reg_error = f"Error: {e}"
        finally:
            self.procesando = False

    @rx.event
    def cerrar_sesion(self):
        """Cierra la sesión y limpia los datos."""
        self.usuario_id = 0
        self.nombre = ""
        self.apellido = ""
        self.email = ""
        self.rol = ""
        self.autenticado = False
        return rx.redirect("/")

    @rx.event
    def proteger_admin(self):
        """Llamar en on_load de páginas de admin. Redirige si no es admin."""
        if not self.autenticado or self.rol != "admin":
            return rx.redirect("/login")

    @rx.event
    def proteger_cliente(self):
        """Llamar en on_load de páginas que requieren login."""
        if not self.autenticado:
            return rx.redirect("/login")
