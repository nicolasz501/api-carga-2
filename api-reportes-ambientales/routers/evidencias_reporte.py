
from fastapi import APIRouter, HTTPException, Query, Depends

from repositories import evidencias_reporte as repo
from repositories import reportes_ambientales as reportes_repo
from models.evidencias_reporte import (
    EvidenciasReporteCrear,
    EvidenciasReporteActualizar,
)
from security.permisos import (
    CIUDADANO,
    FUNCIONARIO_AMBIENTAL,
    ADMINISTRADOR,
    requiere_rol,
)

router = APIRouter(
    prefix="/evidencias-reporte",
    tags=["Evidencias de reportes"],
)


def obtener_evidencia(registro_id: int):
    fila = repo.obtener_registro(registro_id)

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Evidencia no encontrada",
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
            detail="No tienes permiso para acceder a este reporte",
        )

    return reporte


def comprobar_acceso_evidencia(evidencia: dict, usuario: dict):
    reporte_id = evidencia.get("reporte_id")

    if reporte_id is None:
        raise HTTPException(
            status_code=500,
            detail="La evidencia no tiene asociado un reporte",
        )

    comprobar_acceso_reporte(reporte_id, usuario)


# ==========================================
# LISTAR EVIDENCIAS
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
    evidencias = repo.listar_registros(limite, desplazamiento)

    if usuario["rol_id"] == ADMINISTRADOR:
        return evidencias

    if usuario["rol_id"] == FUNCIONARIO_AMBIENTAL:
        return evidencias

    # Los ciudadanos solo ven evidencias de sus propios reportes.
    resultado = []

    for evidencia in evidencias:
        reporte_id = evidencia.get("reporte_id")

        if reporte_id is None:
            continue

        reporte = reportes_repo.obtener_registro(reporte_id)

        if (
            reporte is not None
            and reporte.get("usuario_id") == usuario["usuario_id"]
        ):
            resultado.append(evidencia)

    return resultado


# ==========================================
# OBTENER EVIDENCIA
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
    evidencia = obtener_evidencia(registro_id)
    comprobar_acceso_evidencia(evidencia, usuario)
    return evidencia


# ==========================================
# CREAR EVIDENCIA
# ==========================================
@router.post("/", status_code=201)
def crear(
    datos: EvidenciasReporteCrear,
    usuario: dict = Depends(
        requiere_rol(CIUDADANO, FUNCIONARIO_AMBIENTAL, ADMINISTRADOR)
    ),
):
    valores = datos.model_dump(exclude_unset=True)
    reporte_id = valores.get("reporte_id")

    if reporte_id is None:
        raise HTTPException(
            status_code=400,
            detail="Debes indicar el reporte asociado a la evidencia",
        )

    comprobar_acceso_reporte(reporte_id, usuario)

    try:
        return repo.crear_registro(valores)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No se pudo crear la evidencia",
        )


# ==========================================
# ACTUALIZAR EVIDENCIA
# ==========================================
@router.put("/{registro_id}")
def actualizar(
    registro_id: int,
    datos: EvidenciasReporteActualizar,
    usuario: dict = Depends(
        requiere_rol(CIUDADANO, FUNCIONARIO_AMBIENTAL, ADMINISTRADOR)
    ),
):
    evidencia = obtener_evidencia(registro_id)
    comprobar_acceso_evidencia(evidencia, usuario)

    valores = datos.model_dump(exclude_unset=True)

    # Evitar trasladar una evidencia a otro reporte sin autorización.
    nuevo_reporte_id = valores.get("reporte_id")

    if nuevo_reporte_id is not None:
        comprobar_acceso_reporte(nuevo_reporte_id, usuario)

    try:
        actualizada = repo.actualizar_registro(registro_id, valores)

        if actualizada is None:
            raise HTTPException(
                status_code=404,
                detail="Evidencia no encontrada",
            )

        return actualizada

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ==========================================
# ELIMINAR EVIDENCIA
# ==========================================
@router.delete("/{registro_id}")
def eliminar(
    registro_id: int,
    usuario: dict = Depends(
        requiere_rol(CIUDADANO, FUNCIONARIO_AMBIENTAL, ADMINISTRADOR)
    ),
):
    evidencia = obtener_evidencia(registro_id)
    comprobar_acceso_evidencia(evidencia, usuario)

    try:
        eliminada = repo.eliminar_registro(registro_id)

        if eliminada is None:
            raise HTTPException(
                status_code=404,
                detail="Evidencia no encontrada",
            )

        return {
            "mensaje": "Evidencia eliminada correctamente",
            "registro": eliminada,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No se pudo eliminar la evidencia",
        )
