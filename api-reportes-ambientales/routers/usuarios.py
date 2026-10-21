
from typing import Optional

import bcrypt
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, EmailStr, Field

from repositories import usuarios as repo
from security.permisos import (
    CIUDADANO,
    FUNCIONARIO_AMBIENTAL,
    ADMINISTRADOR,
    crear_token,
    obtener_usuario_actual,
    requiere_rol,
)

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)


# =========================================================
# MODELOS
# =========================================================

class LoginDatos(BaseModel):
    correo: EmailStr
    contrasena: str = Field(min_length=1, max_length=128)


class UsuarioCrear(BaseModel):
    nombres: str = Field(min_length=1, max_length=100)
    apellidos: str = Field(min_length=1, max_length=100)
    correo: EmailStr
    contrasena: str = Field(min_length=8, max_length=128)
    rol_id: int = Field(ge=1)
    telefono: Optional[str] = Field(default=None, max_length=30)
    documento: Optional[str] = Field(default=None, max_length=50)
    estado: bool = True


class UsuarioActualizar(BaseModel):
    nombres: Optional[str] = Field(default=None, min_length=1, max_length=100)
    apellidos: Optional[str] = Field(default=None, min_length=1, max_length=100)
    correo: Optional[EmailStr] = None
    contrasena: Optional[str] = Field(default=None, min_length=8, max_length=128)
    rol_id: Optional[int] = Field(default=None, ge=1)
    telefono: Optional[str] = Field(default=None, max_length=30)
    documento: Optional[str] = Field(default=None, max_length=50)
    estado: Optional[bool] = None


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def limpiar_usuario(usuario: dict) -> dict:
    """Evita enviar el hash de la contraseña al frontend."""
    if not usuario:
        return usuario

    resultado = dict(usuario)
    resultado.pop("contrasena_hash", None)
    return resultado


def obtener_usuario_o_error(usuario_id: int):
    usuario = repo.obtener_registro(usuario_id)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado.",
        )

    return usuario


def comprobar_acceso(usuario_objetivo: dict, usuario_actual: dict):
    if usuario_actual["rol_id"] == ADMINISTRADOR:
        return

    if int(usuario_objetivo["usuario_id"]) != int(usuario_actual["usuario_id"]):
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para acceder a este usuario.",
        )


def validar_rol(rol_id: int):
    """Verifica que el rol exista en la tabla roles."""
    roles_validos = {
        CIUDADANO,
        FUNCIONARIO_AMBIENTAL,
        ADMINISTRADOR,
    }

    if rol_id not in roles_validos:
        raise HTTPException(
            status_code=400,
            detail="El rol seleccionado no es válido.",
        )


def generar_hash(contrasena: str) -> str:
    return bcrypt.hashpw(
        contrasena.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


# =========================================================
# LOGIN
# =========================================================

@router.post("/login")
def iniciar_sesion(datos: LoginDatos):
    usuario = repo.obtener_por_correo(str(datos.correo).strip())

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos.",
        )

    estado = usuario.get("estado")

    estado_activo = (
        estado is True
        or estado == 1
        or (
            isinstance(estado, str)
            and estado.strip().upper() in (
                "ACTIVO",
                "ACTIVA",
                "TRUE",
                "1",
            )
        )
    )

    if not estado_activo:
        raise HTTPException(
            status_code=403,
            detail="Tu cuenta está inactiva. Contacta al administrador.",
        )

    hash_guardado = usuario.get("contrasena_hash")

    if not hash_guardado:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos.",
        )

    try:
        hash_bytes = (
            hash_guardado.encode("utf-8")
            if isinstance(hash_guardado, str)
            else hash_guardado
        )

        contrasena_valida = bcrypt.checkpw(
            datos.contrasena.encode("utf-8"),
            hash_bytes,
        )
    except (ValueError, TypeError):
        contrasena_valida = False

    if not contrasena_valida:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos.",
        )

    usuario_id = usuario["usuario_id"]
    rol_id = usuario["rol_id"]

    token = crear_token(
        usuario_id=usuario_id,
        rol_id=rol_id,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "usuario_id": usuario_id,
            "nombres": usuario.get("nombres"),
            "apellidos": usuario.get("apellidos"),
            "correo": usuario.get("correo"),
            "rol_id": rol_id,
        },
    }


# =========================================================
# LISTAR USUARIOS: SOLO ADMINISTRADOR
# =========================================================

@router.get("/")
def listar(
    limite: int = Query(100, ge=1, le=500),
    desplazamiento: int = Query(0, ge=0),
    usuario_actual: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    usuarios = repo.listar_registros(limite, desplazamiento)

    return [
        limpiar_usuario(usuario)
        for usuario in usuarios
    ]


# =========================================================
# OBTENER USUARIO
# =========================================================

@router.get("/{registro_id}")
def obtener(
    registro_id: int,
    usuario_actual: dict = Depends(
        requiere_rol(
            CIUDADANO,
            FUNCIONARIO_AMBIENTAL,
            ADMINISTRADOR,
        )
    ),
):
    usuario = obtener_usuario_o_error(registro_id)
    comprobar_acceso(usuario, usuario_actual)

    return limpiar_usuario(usuario)


# =========================================================
# CREAR USUARIO: SOLO ADMINISTRADOR
# =========================================================

@router.post("/", status_code=201)
def crear(
    datos: UsuarioCrear,
    usuario_actual: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    validar_rol(datos.rol_id)

    correo = str(datos.correo).strip()

    if repo.obtener_por_correo(correo):
        raise HTTPException(
            status_code=409,
            detail="Ya existe un usuario registrado con ese correo.",
        )

    valores = {
        "nombres": datos.nombres.strip(),
        "apellidos": datos.apellidos.strip(),
        "correo": correo,
        "contrasena_hash": generar_hash(datos.contrasena),
        "rol_id": datos.rol_id,
        "telefono": datos.telefono.strip() if datos.telefono else None,
        "documento": datos.documento.strip() if datos.documento else None,
        "estado": datos.estado,
    }

    try:
        creado = repo.crear_registro(valores)
        return limpiar_usuario(creado)

    except HTTPException:
        raise
    except Exception as exc:
        # El detalle técnico se conserva en el servidor.
        print(f"Error al crear usuario: {exc}")

        raise HTTPException(
            status_code=400,
            detail="No se pudo crear el usuario. Verifica los datos.",
        )


# =========================================================
# ACTUALIZAR USUARIO
# =========================================================

@router.put("/{registro_id}")
def actualizar(
    registro_id: int,
    datos: UsuarioActualizar,
    usuario_actual: dict = Depends(
        requiere_rol(
            CIUDADANO,
            FUNCIONARIO_AMBIENTAL,
            ADMINISTRADOR,
        )
    ),
):
    usuario_existente = obtener_usuario_o_error(registro_id)
    comprobar_acceso(usuario_existente, usuario_actual)

    valores_recibidos = datos.model_dump(exclude_unset=True)

    es_admin = usuario_actual["rol_id"] == ADMINISTRADOR

    # Un ciudadano o funcionario solo puede actualizar sus datos
    # personales. No puede cambiar su rol, estado ni contraseña
    # mediante este endpoint.
    if not es_admin:
        campos_permitidos = {
            "nombres",
            "apellidos",
            "correo",
            "telefono",
        }

        valores_recibidos = {
            campo: valor
            for campo, valor in valores_recibidos.items()
            if campo in campos_permitidos
        }

    if "rol_id" in valores_recibidos:
        if valores_recibidos["rol_id"] is not None:
            validar_rol(valores_recibidos["rol_id"])

    if "correo" in valores_recibidos and valores_recibidos["correo"]:
        correo_nuevo = str(valores_recibidos["correo"]).strip()
        otro_usuario = repo.obtener_por_correo(correo_nuevo)

        if (
            otro_usuario
            and int(otro_usuario["usuario_id"]) != registro_id
        ):
            raise HTTPException(
                status_code=409,
                detail="Ese correo ya está registrado.",
            )

        valores_recibidos["correo"] = correo_nuevo

    # El frontend envía "contrasena"; la base de datos almacena
    # exclusivamente "contrasena_hash".
    contrasena_nueva = valores_recibidos.pop("contrasena", None)

    if contrasena_nueva:
        if not es_admin:
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para cambiar la contraseña.",
            )

        valores_recibidos["contrasena_hash"] = generar_hash(
            contrasena_nueva
        )

    # Nunca aceptar un hash directamente desde el cliente.
    valores_recibidos.pop("contrasena_hash", None)

    if "nombres" in valores_recibidos and valores_recibidos["nombres"]:
        valores_recibidos["nombres"] = valores_recibidos["nombres"].strip()

    if "apellidos" in valores_recibidos and valores_recibidos["apellidos"]:
        valores_recibidos["apellidos"] = valores_recibidos["apellidos"].strip()

    if valores_recibidos.get("telefono"):
        valores_recibidos["telefono"] = valores_recibidos["telefono"].strip()

    if valores_recibidos.get("documento"):
        valores_recibidos["documento"] = valores_recibidos["documento"].strip()

    try:
        actualizado = repo.actualizar_registro(
            registro_id,
            valores_recibidos,
        )

        if actualizado is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado.",
            )

        return limpiar_usuario(actualizado)

    except HTTPException:
        raise
    except Exception as exc:
        print(f"Error al actualizar usuario: {exc}")

        raise HTTPException(
            status_code=400,
            detail="No se pudo actualizar el usuario.",
        )


# =========================================================
# ELIMINAR USUARIO: SOLO ADMINISTRADOR
# =========================================================

@router.delete("/{registro_id}")
def eliminar(
    registro_id: int,
    usuario_actual: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    obtener_usuario_o_error(registro_id)

    # Evita eliminar accidentalmente la cuenta con la que se inició sesión.
    if int(usuario_actual["usuario_id"]) == registro_id:
        raise HTTPException(
            status_code=400,
            detail="No puedes eliminar tu propia cuenta de administrador.",
        )

    try:
        eliminado = repo.eliminar_registro(registro_id)

        if eliminado is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado.",
            )

        return {
            "mensaje": "Usuario eliminado correctamente.",
            "registro": limpiar_usuario(eliminado),
        }

    except HTTPException:
        raise
    except Exception as exc:
        print(f"Error al eliminar usuario: {exc}")

        raise HTTPException(
            status_code=400,
            detail=(
                "No se pudo eliminar el usuario. Puede tener "
                "reportes u otros registros asociados."
            ),
        )
