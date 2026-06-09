"""
Módulo de autenticación y seguridad de contraseñas.

Funciones disponibles:
- hash_password(password): Convierte una contraseña en texto plano
  a un hash seguro usando bcrypt (estándar de la industria).
- verify_password(plain, hashed): Verifica si una contraseña en texto
  coincide con un hash previamente almacenado.

Por seguridad, las contraseñas NUNCA se almacenan en texto plano en la BD.
Solo se guarda el hash generado por bcrypt, que es irreversible.
"""

from passlib.context import CryptContext

# Contexto de hash. bcrypt es el estándar de la industria.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Convierte una contraseña en texto plano a un hash seguro."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña en texto coincide con el hash guardado."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False
