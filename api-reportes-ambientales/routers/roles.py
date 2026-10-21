
from fastapi import APIRouter, HTTPException, Query, Depends

from repositories import roles as repo
from models.roles import RolesCrear, RolesActualizar
from security.permisos import (
    CIUDADANO,
    FUNCIONARIO_AMBIENTAL,
    ADMINISTRADOR,
    requiere_rol,
)

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


# ==========================================
# LISTAR ROLES
# Acceso para todos los usuarios autenticados
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
    return repo.listar_registros(limite, desplazamiento)


# ==========================================
# OBTENER UN ROL
# Acceso para todos los usuarios autenticados
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
    fila = repo.obtener_registro(registro_id)

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado",
        )

    return fila


# ==========================================
# CREAR ROL
# Solo administrador
# ==========================================
@router.post("/", status_code=201)
def crear(
    datos: RolesCrear,
    usuario: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    try:
        return repo.crear_registro(
            datos.model_dump(exclude_unset=True)
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No se pudo crear el rol",
        )


# ==========================================
# ACTUALIZAR ROL
# Solo administrador
# ==========================================
@router.put("/{registro_id}")
def actualizar(
    registro_id: int,
    datos: RolesActualizar,
    usuario: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    try:
        fila = repo.actualizar_registro(
            registro_id,
            datos.model_dump(exclude_unset=True),
        )

        if fila is None:
            raise HTTPException(
                status_code=404,
                detail="Rol no encontrado",
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
            detail="No se pudo actualizar el rol",
        )


# ==========================================
# ELIMINAR ROL
# Solo administrador
# ==========================================
@router.delete("/{registro_id}")
def eliminar(
    registro_id: int,
    usuario: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    try:
        fila = repo.eliminar_registro(registro_id)

        if fila is None:
            raise HTTPException(
                status_code=404,
                detail="Rol no encontrado",
            )

        return {
            "mensaje": "Rol eliminado correctamente",
            "registro": fila,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail=(
                "No se pudo eliminar el rol. "
                "Verifica si existen usuarios o permisos asociados."
            ),
        )
