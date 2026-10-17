
from fastapi import APIRouter, HTTPException

from app.models.ModuloRol import ModuloRol
from app.repositories.modulo_rol_repository import ModuloRolRepository


router = APIRouter(
    prefix="/modulos-rol",
    tags=["Gestión de Módulos por Rol"]
)

repo = ModuloRolRepository()


@router.get("/")
def listar_modulos_rol():
    try:
        return repo.obtener_todos()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar los módulos por rol"
        )


@router.get("/{id_modulos_rol}")
def obtener_modulo_rol(id_modulos_rol: int):
    try:
        modulo_rol = repo.obtener_por_id(id_modulos_rol)

        if not modulo_rol:
            raise HTTPException(
                status_code=404,
                detail="Módulo-Rol no encontrado"
            )

        return modulo_rol

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar el módulo por rol"
        )


@router.post("/", status_code=201)
def crear_modulo_rol(modulo_rol: ModuloRol):
    try:
        nuevo_id = repo.crear(modulo_rol)

        return {
            "mensaje": "Módulo-Rol registrado exitosamente",
            "id_modulos_rol": nuevo_id
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo registrar el módulo por rol. Verifica que el rol y el módulo existan."
        )


@router.put("/{id_modulos_rol}")
def actualizar_modulo_rol(
    id_modulos_rol: int,
    modulo_rol: ModuloRol
):
    try:
        actualizado = repo.actualizar(
            id_modulos_rol,
            modulo_rol
        )

        if not actualizado:
            raise HTTPException(
                status_code=404,
                detail="Módulo-Rol no encontrado"
            )

        return {
            "mensaje": "Módulo-Rol actualizado correctamente"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar el módulo por rol"
        )


@router.delete("/{id_modulos_rol}")
def eliminar_modulo_rol(id_modulos_rol: int):
    try:
        eliminado = repo.eliminar(id_modulos_rol)

        if not eliminado:
            raise HTTPException(
                status_code=404,
                detail="Módulo-Rol no encontrado"
            )

        return {
            "mensaje": "Módulo-Rol eliminado correctamente"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo eliminar el módulo por rol"
        )
