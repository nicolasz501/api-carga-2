
from fastapi import APIRouter, HTTPException, Query, Depends

from repositories import validaciones_reporte as repo
from repositories import reportes_ambientales as reportes_repo

from models.validaciones_reporte import (
    ValidacionesReporteCrear,
    ValidacionesReporteActualizar,
)

from security.permisos import (
    CIUDADANO,
    FUNCIONARIO_AMBIENTAL,
    ADMINISTRADOR,
    requiere_rol,
)

router = APIRouter(
    prefix="/validaciones-reporte",
    tags=["Validaciones de reportes"],
)


def obtener_validacion_o_error(registro_id: int):
    fila = repo.obtener_registro(registro_id)

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Validación no encontrada",
        )

    return fila


def obtener_reporte_o_error(reporte_id: int):
    reporte = reportes_repo.obtener_registro(reporte_id)

    if reporte is None:
        raise HTTPException(
            status_code=404,
            detail="Reporte ambiental no encontrado",
        )

    return reporte


def comprobar_acceso_reporte(reporte: dict, usuario: dict):
    if usuario["rol_id"] in (
        FUNCIONARIO_AMBIENTAL,
        ADMINISTRADOR,
    ):
        return

    if reporte.get("usuario_id") != usuario["usuario_id"]:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para consultar esta validación",
        )


def comprobar_acceso_validacion(validacion: dict, usuario: dict):
    reporte_id = validacion.get("reporte_id")

    if reporte_id is None:
        raise HTTPException(
            status_code=500,
            detail="La validación no contiene el identificador del reporte",
        )

    reporte = obtener_reporte_o_error(reporte_id)
    comprobar_acceso_reporte(reporte, usuario)


# ==========================================
# LISTAR VALIDACIONES
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
    validaciones = repo.listar_registros(limite, desplazamiento)

    if usuario["rol_id"] in (
        FUNCIONARIO_AMBIENTAL,
        ADMINISTRADOR,
    ):
        return validaciones

    # El ciudadano solo puede consultar las validaciones
    # de los reportes de su propiedad.
    resultado = []

    for validacion in validaciones:
        reporte_id = validacion.get("reporte_id")

        if reporte_id is None:
            continue

        reporte = reportes_repo.obtener_registro(reporte_id)

        if (
            reporte is not None
            and reporte.get("usuario_id") == usuario["usuario_id"]
        ):
            resultado.append(validacion)

    return resultado


# ==========================================
# OBTENER UNA VALIDACIÓN
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
    validacion = obtener_validacion_o_error(registro_id)
    comprobar_acceso_validacion(validacion, usuario)

    return validacion


# ==========================================
# CREAR VALIDACIÓN
# Funcionario ambiental y administrador
# ==========================================
@router.post("/", status_code=201)
def crear(
    datos: ValidacionesReporteCrear,
    usuario: dict = Depends(
        requiere_rol(
            FUNCIONARIO_AMBIENTAL,
            ADMINISTRADOR,
        )
    ),
):
    valores = datos.model_dump(exclude_unset=True)

    reporte_id = valores.get("reporte_id")

    if reporte_id is None:
        raise HTTPException(
            status_code=400,
            detail="Debes indicar el reporte que se va a validar",
        )

    obtener_reporte_o_error(reporte_id)

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
            detail="No se pudo crear la validación del reporte",
        )


# ==========================================
# ACTUALIZAR VALIDACIÓN
# Funcionario ambiental y administrador
# ==========================================
@router.put("/{registro_id}")
def actualizar(
    registro_id: int,
    datos: ValidacionesReporteActualizar,
    usuario: dict = Depends(
        requiere_rol(
            FUNCIONARIO_AMBIENTAL,
            ADMINISTRADOR,
        )
    ),
):
    validacion = obtener_validacion_o_error(registro_id)

    # Si el modelo permite cambiar el reporte relacionado,
    # también se comprueba que el nuevo reporte exista.
    valores = datos.model_dump(exclude_unset=True)

    reporte_id = valores.get(
        "reporte_id",
        validacion.get("reporte_id"),
    )

    if reporte_id is not None:
        obtener_reporte_o_error(reporte_id)

    try:
        actualizado = repo.actualizar_registro(
            registro_id,
            valores,
        )

        if actualizado is None:
            raise HTTPException(
                status_code=404,
                detail="Validación no encontrada",
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
            detail="No se pudo actualizar la validación",
        )


# ==========================================
# ELIMINAR VALIDACIÓN
# Solo administrador
# ==========================================
@router.delete("/{registro_id}")
def eliminar(
    registro_id: int,
    usuario: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    obtener_validacion_o_error(registro_id)

    try:
        fila = repo.eliminar_registro(registro_id)

        if fila is None:
            raise HTTPException(
                status_code=404,
                detail="Validación no encontrada",
            )

        return {
            "mensaje": "Validación eliminada correctamente",
            "registro": fila,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail=(
                "No se pudo eliminar la validación. "
                "Verifica las relaciones existentes en la base de datos."
            ),
        )
