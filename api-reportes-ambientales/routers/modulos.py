
from fastapi import APIRouter, HTTPException, Query, Depends

from repositories import modulos as repo
from models.modulos import ModulosCrear, ModulosActualizar
from security.permisos import (
    CIUDADANO,
    FUNCIONARIO_AMBIENTAL,
    ADMINISTRADOR,
    requiere_rol,
)

router = APIRouter(
    prefix="/modulos",
    tags=["Módulos"],
)


# ==========================================
# LISTAR MÓDULOS
# Ciudadano, funcionario y administrador
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
# OBTENER UN MÓDULO
# Ciudadano, funcionario y administrador
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
            detail="Módulo no encontrado",
        )

    return fila


# ==========================================
# CREAR MÓDULO
# Solo administrador
# ==========================================
@router.post("/", status_code=201)
def crear(
    datos: ModulosCrear,
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
            detail="No se pudo crear el módulo",
        )


# ==========================================
# ACTUALIZAR MÓDULO
# Solo administrador
# ==========================================
@router.put("/{registro_id}")
def actualizar(
    registro_id: int,
    datos: ModulosActualizar,
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
                detail="Módulo no encontrado",
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
            detail="No se pudo actualizar el módulo",
        )


# ==========================================
# ELIMINAR MÓDULO
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
                detail="Módulo no encontrado",
            )

        return {
            "mensaje": "Módulo eliminado correctamente",
            "registro": fila,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail=(
                "No se pudo eliminar el módulo. "
                "Puede tener permisos de roles asociados."
            ),
        )
