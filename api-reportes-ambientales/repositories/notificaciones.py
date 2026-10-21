
from repositories import base


TABLA = "notificaciones"
PK = "notificacion_id"

COLUMNAS = [
    "usuario_id",
    "reporte_id",
    "titulo",
    "mensaje",
    "leida",
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
    # Las fechas de creación y lectura no se modifican directamente.
    datos_permitidos = {
        campo: valor
        for campo, valor in datos.items()
        if campo in ("usuario_id", "reporte_id", "titulo", "mensaje", "leida")
    }

    return base.actualizar(
        TABLA,
        PK,
        valor,
        datos_permitidos,
        COLUMNAS,
    )


def eliminar_registro(valor):
    return base.eliminar(
        TABLA,
        PK,
        valor,
    )
