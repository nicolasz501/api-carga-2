
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

if not JWT_SECRET_KEY:
    raise RuntimeError("Falta configurar JWT_SECRET_KEY en .env")

bearer = HTTPBearer(auto_error=False)

# IDs de roles definidos en la base de datos.
CIUDADANO = 1
FUNCIONARIO_AMBIENTAL = 2
ADMINISTRADOR = 3


def crear_token(usuario_id: int, rol_id: int) -> str:
    ahora = datetime.now(timezone.utc)

    datos = {
        "sub": str(usuario_id),
        "rol_id": rol_id,
        "iat": ahora,
        "exp": ahora + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }

    return jwt.encode(datos, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(bearer),
):
    if credenciales is None:
        raise HTTPException(
            status_code=401,
            detail="Debes iniciar sesión para acceder a este recurso.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        datos = jwt.decode(
            credenciales.credentials,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        usuario_id = int(datos["sub"])
        rol_id = int(datos["rol_id"])

        return {
            "usuario_id": usuario_id,
            "rol_id": rol_id,
        }

    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="El token es inválido o ha expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def requiere_rol(*roles_permitidos: int):
    def verificar_rol(
        usuario: dict = Depends(obtener_usuario_actual),
    ):
        if usuario["rol_id"] not in roles_permitidos:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para realizar esta operación.",
            )

        return usuario

    return verificar_rol
