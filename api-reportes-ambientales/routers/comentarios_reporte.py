
from fastapi import APIRouter, HTTPException, Query, Depends

from repositories import comentarios_reporte as repo
from models.comentarios_reporte import (
    ComentariosReporteCrear,
    ComentariosReporteActualizar,
)
from security.permisos import (
    CIUDADANO,
    FUNCIONARIO_AMBIENTAL,
    ADMINISTRADOR,
    requiere_rol,
)

router = APIRouter(
    prefix="/comentarios-reporte",
    tags=["Comentarios de reportes"],
)


def obtener_comentario_o_error(registro_id: int):
    fila = repo.obtener_registro(registro_id)

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Comentario no encontrado",
        )

    return fila


def comprobar_propiedad(fila: dict, usuario: dict):
    # Los funcionarios y administradores pueden gestionar comentarios
    # según los permisos definidos para sus roles.
    if usuario["rol_id"] == ADMINISTRADOR:
        return

    if usuario["rol_id"] == FUNCIONARIO_AMBIENTAL:
        return

    if fila.get("usuario_id") != usuario["usuario_id"]:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para gestionar este comentario",
        )


# ==========================================
# LISTAR COMENTARIOS
# Acceso para los tres roles
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
    comentarios = repo.listar_registros(limite, desplazamiento)

    # Los ciudadanos solo reciben sus propios comentarios.
    if usuario["rol_id"] == CIUDADANO:
        return [
            comentario
            for comentario in comentarios
            if comentario.get("usuario_id") == usuario["usuario_id"]
        ]

    return comentarios


# ==========================================
# OBTENER UN COMENTARIO
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
    fila = obtener_comentario_o_error(registro_id)
    comprobar_propiedad(fila, usuario)
    return fila


# ==========================================
# CREAR COMENTARIO
# Ciudadano y administrador
# ==========================================
@router.post("/", status_code=201)
def crear(
    datos: ComentariosReporteCrear,
    usuario: dict = Depends(
        requiere_rol(CIUDADANO, ADMINISTRADOR)
    ),
):
    valores = datos.model_dump(exclude_unset=True)

    # No permitir que el usuario cree comentarios en nombre de otra persona.
    if usuario["rol_id"] == CIUDADANO:
        valores["usuario_id"] = usuario["usuario_id"]

    try:
        return repo.crear_registro(valores)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No se pudo crear el comentario",
        )


# ==========================================
# ACTUALIZAR COMENTARIO
# Ciudadano: propio
# Funcionario y administrador: según su rol
# ==========================================
@router.put("/{registro_id}")
def actualizar(
    registro_id: int,
    datos: ComentariosReporteActualizar,
    usuario: dict = Depends(
        requiere_rol(
            CIUDADANO,
            FUNCIONARIO_AMBIENTAL,
            ADMINISTRADOR,
        )
    ),
):
    fila = obtener_comentario_o_error(registro_id)
    comprobar_propiedad(fila, usuario)

    valores = datos.model_dump(exclude_unset=True)

    # Impedir cambiar el propietario del comentario.
    valores.pop("usuario_id", None)

    try:
        actualizado = repo.actualizar_registro(registro_id, valores)

        if actualizado is None:
            raise HTTPException(
                status_code=404,
                detail="Comentario no encontrado",
            )

        return actualizado

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ==========================================
# ELIMINAR COMENTARIO
# Ciudadano: propio
# Funcionario y administrador: según su rol
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
    fila = obtener_comentario_o_error(registro_id)
    comprobar_propiedad(fila, usuario)

    try:
        eliminado = repo.eliminar_registro(registro_id)

        if eliminado is None:
            raise HTTPException(
                status_code=404,
                detail="Comentario no encontrado",
            )

        return {
            "mensaje": "Comentario eliminado correctamente",
            "registro": eliminado,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No se pudo eliminar el comentario",
        )
