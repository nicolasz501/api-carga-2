
from fastapi import APIRouter, HTTPException, Query, Depends

from repositories import modulos_por_rol as repo
from models.modulos_por_rol import (
    ModulosPorRolCrear,
    ModulosPorRolActualizar,
)
from security.permisos import (
    ADMINISTRADOR,
    requiere_rol,
)

router = APIRouter(
    prefix="/modulos-por-rol",
    tags=["Módulos y permisos por rol"],
)


# ==========================================
# LISTAR PERMISOS
# Solo administrador
# ==========================================
@router.get("/")
def listar(
    limite: int = Query(100, ge=1, le=500),
    desplazamiento: int = Query(0, ge=0),
    usuario: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    return repo.listar_registros(limite, desplazamiento)


# ==========================================
# OBTENER UN PERMISO
# Solo administrador
# ==========================================
@router.get("/{registro_id}")
def obtener(
    registro_id: int,
    usuario: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    fila = repo.obtener_registro(registro_id)

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Configuración de permisos no encontrada",
        )

    return fila


# ==========================================
# CREAR PERMISO
# Solo administrador
# ==========================================
@router.post("/", status_code=201)
def crear(
    datos: ModulosPorRolCrear,
    usuario: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    try:
        valores = datos.model_dump(exclude_unset=True)

        # Evitar configuraciones contradictorias.
        puede_crear = valores.get("puede_crear", False)
        puede_editar = valores.get("puede_editar", False)
        puede_eliminar = valores.get("puede_eliminar", False)
        puede_ver = valores.get("puede_ver", False)

        if (puede_crear or puede_editar or puede_eliminar) and not puede_ver:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Para crear, editar o eliminar, "
                    "el permiso de visualización debe estar habilitado."
                ),
            )

        return repo.crear_registro(valores)

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
            detail="No se pudo crear la configuración de permisos",
        )


# ==========================================
# ACTUALIZAR PERMISO
# Solo administrador
# ==========================================
@router.put("/{registro_id}")
def actualizar(
    registro_id: int,
    datos: ModulosPorRolActualizar,
    usuario: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    existente = repo.obtener_registro(registro_id)

    if existente is None:
        raise HTTPException(
            status_code=404,
            detail="Configuración de permisos no encontrada",
        )

    valores = datos.model_dump(exclude_unset=True)

    # Validar la configuración final, combinando los datos actuales
    # con los campos que se quieren modificar.
    configuracion = dict(existente)
    configuracion.update(valores)

    puede_crear = configuracion.get("puede_crear", False)
    puede_editar = configuracion.get("puede_editar", False)
    puede_eliminar = configuracion.get("puede_eliminar", False)
    puede_ver = configuracion.get("puede_ver", False)

    if (puede_crear or puede_editar or puede_eliminar) and not puede_ver:
        raise HTTPException(
            status_code=400,
            detail=(
                "Para crear, editar o eliminar, "
                "el permiso de visualización debe estar habilitado."
            ),
        )

    try:
        fila = repo.actualizar_registro(registro_id, valores)

        if fila is None:
            raise HTTPException(
                status_code=404,
                detail="Configuración de permisos no encontrada",
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
            detail="No se pudo actualizar la configuración de permisos",
        )


# ==========================================
# ELIMINAR PERMISO
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
                detail="Configuración de permisos no encontrada",
            )

        return {
            "mensaje": "Configuración de permisos eliminada correctamente",
            "registro": fila,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail=(
                "No se pudo eliminar la configuración de permisos."
            ),
        )
