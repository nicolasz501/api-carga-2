
from fastapi import APIRouter, HTTPException, Query, Depends

from repositories import notificaciones as repo
from models.notificaciones import (
    NotificacionesCrear,
    NotificacionesActualizar,
)
from security.permisos import (
    CIUDADANO,
    FUNCIONARIO_AMBIENTAL,
    ADMINISTRADOR,
    requiere_rol,
)

router = APIRouter(
    prefix="/notificaciones",
    tags=["Notificaciones"],
)


def obtener_notificacion_o_error(registro_id: int):
    fila = repo.obtener_registro(registro_id)

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Notificación no encontrada",
        )

    return fila


def comprobar_propiedad(fila: dict, usuario: dict):
    if usuario["rol_id"] == ADMINISTRADOR:
        return

    if fila.get("usuario_id") != usuario["usuario_id"]:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para acceder a esta notificación",
        )


# ==========================================
# LISTAR NOTIFICACIONES
# ==========================================
@router.get("/")
def listar(
    limite: int = Query(100, ge=1, le=500),
    desplazamiento: int = Query(0, ge=0),
    usuario: dict = Depends(
        requiere_rol(
            CIUDADANO,
            FUNCIONARIO_AMBIENTAL,
            ADMINISTRADOR,
        )
    ),
):
    notificaciones = repo.listar_registros(limite, desplazamiento)

    if usuario["rol_id"] == ADMINISTRADOR:
        return notificaciones

    # Los demás roles solo ven sus propias notificaciones.
    return [
        notificacion
        for notificacion in notificaciones
        if notificacion.get("usuario_id") == usuario["usuario_id"]
    ]


# ==========================================
# OBTENER UNA NOTIFICACIÓN
# ==========================================
@router.get("/{registro_id}")
def obtener(
    registro_id: int,
    usuario: dict = Depends(
        requiere_rol(
            CIUDADANO,
            FUNCIONARIO_AMBIENTAL,
            ADMINISTRADOR,
        )
    ),
):
    fila = obtener_notificacion_o_error(registro_id)
    comprobar_propiedad(fila, usuario)
    return fila


# ==========================================
# CREAR NOTIFICACIÓN
# Ciudadano, funcionario y administrador
# ==========================================
@router.post("/", status_code=201)
def crear(
    datos: NotificacionesCrear,
    usuario: dict = Depends(
        requiere_rol(
            CIUDADANO,
            FUNCIONARIO_AMBIENTAL,
            ADMINISTRADOR,
        )
    ),
):
    valores = datos.model_dump(exclude_unset=True)

    # Ciudadanos y funcionarios solo pueden generar notificaciones
    # para su propia cuenta.
    if usuario["rol_id"] != ADMINISTRADOR:
        valores["usuario_id"] = usuario["usuario_id"]

    try:
        return repo.crear_registro(valores)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No se pudo crear la notificación",
        )


# ==========================================
# ACTUALIZAR NOTIFICACIÓN
# ==========================================
@router.put("/{registro_id}")
def actualizar(
    registro_id: int,
    datos: NotificacionesActualizar,
    usuario: dict = Depends(
        requiere_rol(
            CIUDADANO,
            FUNCIONARIO_AMBIENTAL,
            ADMINISTRADOR,
        )
    ),
):
    existente = obtener_notificacion_o_error(registro_id)
    comprobar_propiedad(existente, usuario)

    valores = datos.model_dump(exclude_unset=True)

    # No permitir cambiar el destinatario de la notificación.
    valores.pop("usuario_id", None)

    try:
        fila = repo.actualizar_registro(registro_id, valores)

        if fila is None:
            raise HTTPException(
                status_code=404,
                detail="Notificación no encontrada",
            )

        return fila

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No se pudo actualizar la notificación",
        )


# ==========================================
# ELIMINAR NOTIFICACIÓN
# ==========================================
@router.delete("/{registro_id}")
def eliminar(
    registro_id: int,
    usuario: dict = Depends(
        requiere_rol(
            CIUDADANO,
            FUNCIONARIO_AMBIENTAL,
            ADMINISTRADOR,
        )
    ),
):
    existente = obtener_notificacion_o_error(registro_id)
    comprobar_propiedad(existente, usuario)

    try:
        fila = repo.eliminar_registro(registro_id)

        if fila is None:
            raise HTTPException(
                status_code=404,
                detail="Notificación no encontrada",
            )

        return {
            "mensaje": "Notificación eliminada correctamente",
            "registro": fila,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No se pudo eliminar la notificación",
        )
