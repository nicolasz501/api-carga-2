
from fastapi import APIRouter, HTTPException

from app.models.ModuloRol import ModuloRol
from app.repositories.modulo_rol_repository import ModuloRolRepository


router = APIRouter(
    prefix="/modulos-rol",
    tags=["Gestión de Módulos por Rol"]
)

repo = ModuloRolRepository()


def normalizar_permiso(permiso):
    """Adapta la respuesta de PostgreSQL al formato esperado por el frontend."""
    if not permiso:
        return None

    return {
        "modules_rol_id": permiso.get(
            "id_modulos_rol", permiso.get("modules_rol_id")
        ),
        "role_id": permiso.get("id_rol", permiso.get("role_id")),
        "module_id": permiso.get("id_modulos", permiso.get("module_id")),
        "puede_ver": permiso.get("puede_ver", False),
        "puede_crear": permiso.get("puede_crear", False),
        "puede_editar": permiso.get("puede_editar", False),
        "puede_eliminar": permiso.get("puede_eliminar", False),
        "estado": permiso.get("estado", True),
        "created_at": permiso.get("created_at"),
        "updated_at": permiso.get("updated_at"),
    }


@router.get("/")
def listar_modulos_rol():
    try:
        return [
            normalizar_permiso(p)
            for p in repo.obtener_todos()
        ]
    except Exception as e:
        print(f"Error al consultar módulos por rol: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al consultar los módulos por rol"
        )


@router.get("/{id_modulos_rol}")
def obtener_modulo_rol(id_modulos_rol: int):
    try:
        permiso = repo.obtener_por_id(id_modulos_rol)

        if not permiso:
            raise HTTPException(
                status_code=404,
                detail="Módulo-Rol no encontrado"
            )

        return normalizar_permiso(permiso)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al consultar módulo por rol: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al consultar el módulo por rol"
        )


@router.post("/", status_code=201)
def crear_modulo_rol(modulo_rol: ModuloRol):
    try:
        nuevo_id = repo.crear(modulo_rol)

        permiso = repo.obtener_por_id(nuevo_id)

        if not permiso:
            raise HTTPException(
                status_code=500,
                detail="El permiso se creó, pero no se pudo recuperar."
            )

        return normalizar_permiso(permiso)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al crear módulo por rol: {e}")
        raise HTTPException(
            status_code=500,
            detail=(
                "No se pudo registrar el permiso. "
                "Verifica que el rol y el módulo existan."
            )
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

        permiso = repo.obtener_por_id(id_modulos_rol)

        if not permiso:
            raise HTTPException(
                status_code=404,
                detail="No se encontró el permiso actualizado"
            )

        return normalizar_permiso(permiso)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al actualizar módulo por rol: {e}")
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar el permiso"
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
            "mensaje": "Módulo-Rol eliminado correctamente",
            "modules_rol_id": id_modulos_rol
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al eliminar módulo por rol: {e}")
        raise HTTPException(
            status_code=500,
            detail="No se pudo eliminar el permiso"
        )
