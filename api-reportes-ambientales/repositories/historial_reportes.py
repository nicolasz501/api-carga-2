
from repositories import base


TABLA = "historial_reportes"
PK = "historial_id"

COLUMNAS = [
    "reporte_id",
    "usuario_id",
    "estado_anterior_id",
    "estado_nuevo_id",
    "observacion",
]


def listar_registros(limite=100, desplazamiento=0):
    return base.listar(
        TABLA,
        limite,
        desplazamiento,
    )


def obtener_registro(valor):
    return base.obtener_por_id(
        TABLA,
        PK,
        valor,
    )


def crear_registro(datos):
    return base.crear(
        TABLA,
        datos,
        COLUMNAS,
    )


def actualizar_registro(valor, datos):
    # El historial debe conservar los datos del cambio original.
    raise ValueError(
        "El historial de reportes no se puede modificar"
    )


def eliminar_registro(valor):
    # Se conserva la trazabilidad de los cambios realizados.
    raise ValueError(
        "El historial de reportes no se puede eliminar"
    )
