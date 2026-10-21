
from fastapi import APIRouter, HTTPException, Query, Depends
from repositories import estados_reporte as estados_repo
from repositories import reportes_ambientales as repo
from models.reportes_ambientales import (
    ReportesAmbientalesCrear,
    ReportesAmbientalesActualizar,
)
from security.permisos import (
    CIUDADANO,
    FUNCIONARIO_AMBIENTAL,
    ADMINISTRADOR,
    requiere_rol,
)

router = APIRouter(
    prefix="/reportes-ambientales",
    tags=["Reportes ambientales"],
)


def obtener_reporte_o_error(registro_id: int):
    reporte = repo.obtener_registro(registro_id)

    if reporte is None:
        raise HTTPException(
            status_code=404,
            detail="Reporte ambiental no encontrado",
        )

    return reporte


def comprobar_propiedad(reporte: dict, usuario: dict):
    if usuario["rol_id"] == ADMINISTRADOR:
        return

    if usuario["rol_id"] == FUNCIONARIO_AMBIENTAL:
        return

    if reporte.get("usuario_id") != usuario["usuario_id"]:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para acceder a este reporte",
        )


def comprobar_reporte_editable(reporte: dict):
    estado = str(reporte.get("estado_nombre", "")).upper()

    # Se permite editar mientras el reporte siga en RECIBIDO.
    if estado != "RECIBIDO":
        raise HTTPException(
            status_code=409,
            detail=(
                "Este reporte ya está en revisión o gestión "
                "y no puede modificarse ni eliminarse por el ciudadano."
            ),
        )


# ==========================================
# LISTAR REPORTES
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
    reportes = repo.listar_registros(
        limite=limite,
        desplazamiento=desplazamiento,
    )

    if usuario["rol_id"] in (
        FUNCIONARIO_AMBIENTAL,
        ADMINISTRADOR,
    ):
        return reportes

    return [
        reporte
        for reporte in reportes
        if reporte.get("usuario_id") == usuario["usuario_id"]
    ]


# ==========================================
# OBTENER UN REPORTE
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
    reporte = obtener_reporte_o_error(registro_id)
    comprobar_propiedad(reporte, usuario)
    return reporte


# ==========================================
# CREAR REPORTE
# Ciudadano y administrador
# ==========================================
@router.post("/", status_code=201)
def crear(
    datos: ReportesAmbientalesCrear,
    usuario: dict = Depends(
        requiere_rol(CIUDADANO, ADMINISTRADOR)
    ),
):
    valores = datos.model_dump(exclude_unset=True)

    # El usuario se obtiene de la sesión autenticada.
    valores["usuario_id"] = usuario["usuario_id"]

    # El estado inicial lo asigna el backend.
    valores.pop("estado_reporte_id", None)

    try:
        estado_recibido = estados_repo.obtener_por_nombre("RECIBIDO")

        if estado_recibido is None:
            raise HTTPException(
                status_code=500,
                detail="No existe un estado activo llamado RECIBIDO."
            )

        valores["estado_reporte_id"] = (
            estado_recibido["estado_reporte_id"]
        )

        return repo.crear_registro(valores)

    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        print(f"Error al crear reporte ambiental: {exc}")
        raise HTTPException(
            status_code=500,
            detail="No se pudo crear el reporte ambiental."
        )

# ==========================================
# ACTUALIZAR REPORTE
# ==========================================
@router.put("/{registro_id}")
def actualizar(
    registro_id: int,
    datos: ReportesAmbientalesActualizar,
    usuario: dict = Depends(
        requiere_rol(
            CIUDADANO,
            FUNCIONARIO_AMBIENTAL,
            ADMINISTRADOR,
        )
    ),
):
    reporte = obtener_reporte_o_error(registro_id)
    comprobar_propiedad(reporte, usuario)

    valores = datos.model_dump(exclude_unset=True)

    # Nunca permitir cambiar al propietario del reporte.
    valores.pop("usuario_id", None)

    if usuario["rol_id"] == CIUDADANO:
        # Un ciudadano no puede cambiar por sí mismo el estado del reporte.
        valores.pop("estado_reporte_id", None)

        comprobar_reporte_editable(reporte)

    try:
        actualizado = repo.actualizar_registro(registro_id, valores)

        if actualizado is None:
            raise HTTPException(
                status_code=404,
                detail="Reporte ambiental no encontrado",
            )

        return actualizado

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
            detail="No se pudo actualizar el reporte ambiental",
        )


# ==========================================
# ELIMINAR REPORTE
# ==========================================
@router.delete("/{registro_id}")
def eliminar(
    registro_id: int,
    usuario: dict = Depends(
        requiere_rol(
            CIUDADANO,
            ADMINISTRADOR,
        )
    ),
):
    reporte = obtener_reporte_o_error(registro_id)
    comprobar_propiedad(reporte, usuario)

    if usuario["rol_id"] == CIUDADANO:
        comprobar_reporte_editable(reporte)

    try:
        eliminado = repo.eliminar_registro(registro_id)

        if eliminado is None:
            raise HTTPException(
                status_code=404,
                detail="Reporte ambiental no encontrado",
            )

        return {
            "mensaje": "Reporte ambiental eliminado correctamente",
            "registro": eliminado,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail=(
                "No se pudo eliminar el reporte. "
                "Puede tener evidencias, comentarios o historial asociados."
            ),
        )
