
from fastapi import APIRouter, HTTPException, Query, Depends

from repositories import historial_reportes as repo
from repositories import reportes_ambientales as reportes_repo
from models.historial_reportes import (
    HistorialReportesCrear,
    HistorialReportesActualizar,
)
from security.permisos import (
    CIUDADANO,
    FUNCIONARIO_AMBIENTAL,
    ADMINISTRADOR,
    requiere_rol,
)

router = APIRouter(
    prefix="/historial-reportes",
    tags=["Historial de reportes"],
)


def obtener_historial_o_error(registro_id: int):
    fila = repo.obtener_registro(registro_id)

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Registro del historial no encontrado",
        )

    return fila


def comprobar_acceso_reporte(reporte_id: int, usuario: dict):
    reporte = reportes_repo.obtener_registro(reporte_id)

    if reporte is None:
        raise HTTPException(
            status_code=404,
            detail="Reporte ambiental no encontrado",
        )

    if usuario["rol_id"] == ADMINISTRADOR:
        return reporte

    if usuario["rol_id"] == FUNCIONARIO_AMBIENTAL:
        return reporte

    if reporte.get("usuario_id") != usuario["usuario_id"]:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para consultar este historial",
        )

    return reporte


def comprobar_acceso_historial(fila: dict, usuario: dict):
    reporte_id = fila.get("reporte_id")

    if reporte_id is None:
        raise HTTPException(
            status_code=500,
            detail="El registro del historial no tiene un reporte asociado",
        )

    comprobar_acceso_reporte(reporte_id, usuario)


# ==========================================
# LISTAR HISTORIAL
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
    registros = repo.listar_registros(limite, desplazamiento)

    if usuario["rol_id"] in (FUNCIONARIO_AMBIENTAL, ADMINISTRADOR):
        return registros

    # El ciudadano únicamente puede consultar el historial de sus reportes.
    resultado = []

    for fila in registros:
        reporte_id = fila.get("reporte_id")

        if reporte_id is None:
            continue

        reporte = reportes_repo.obtener_registro(reporte_id)

        if (
            reporte is not None
            and reporte.get("usuario_id") == usuario["usuario_id"]
        ):
            resultado.append(fila)

    return resultado


# ==========================================
# OBTENER UN REGISTRO DEL HISTORIAL
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
    fila = obtener_historial_o_error(registro_id)
    comprobar_acceso_historial(fila, usuario)
    return fila


# ==========================================
# REGISTRAR UN CAMBIO EN EL HISTORIAL
# Funcionario y administrador
# ==========================================
@router.post("/", status_code=201)
def crear(
    datos: HistorialReportesCrear,
    usuario: dict = Depends(
        requiere_rol(FUNCIONARIO_AMBIENTAL, ADMINISTRADOR)
    ),
):
    valores = datos.model_dump(exclude_unset=True)
    reporte_id = valores.get("reporte_id")

    if reporte_id is None:
        raise HTTPException(
            status_code=400,
            detail="Debes indicar el reporte asociado al historial",
        )

    comprobar_acceso_reporte(reporte_id, usuario)

    # El usuario que ejecuta la operación queda registrado como autor.
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
            detail="No se pudo registrar el cambio en el historial",
        )


# ==========================================
# ACTUALIZAR HISTORIAL
# Solo administrador
# ==========================================
@router.put("/{registro_id}")
def actualizar(
    registro_id: int,
    datos: HistorialReportesActualizar,
    usuario: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    obtener_historial_o_error(registro_id)

    valores = datos.model_dump(exclude_unset=True)

    try:
        fila = repo.actualizar_registro(registro_id, valores)

        if fila is None:
            raise HTTPException(
                status_code=404,
                detail="Registro del historial no encontrado",
            )

        return fila

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


# ==========================================
# ELIMINAR HISTORIAL
# Solo administrador
# ==========================================
@router.delete("/{registro_id}")
def eliminar(
    registro_id: int,
    usuario: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    obtener_historial_o_error(registro_id)

    try:
        fila = repo.eliminar_registro(registro_id)

        if fila is None:
            raise HTTPException(
                status_code=404,
                detail="Registro del historial no encontrado",
            )

        return {
            "mensaje": "Registro del historial eliminado correctamente",
            "registro": fila,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No se pudo eliminar el registro del historial",
        )
