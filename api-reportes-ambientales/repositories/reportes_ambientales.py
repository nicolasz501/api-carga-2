from repositories import base

TABLA = "reportes_ambientales"
PK = "reporte_id"

COLUMNAS = [
    "usuario_id",
    "categoria_id",
    "zona_id",
    "estado_reporte_id",
    "titulo",
    "descripcion",
    "direccion_referencia",
    "latitud",
    "longitud",
    "fecha_incidente",
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
    if not datos:
        raise ValueError("No hay campos para actualizar")

    return base.actualizar(
        TABLA,
        PK,
        valor,
        datos,
        COLUMNAS,
    )


def eliminar_registro(valor):
    return base.eliminar(
        TABLA,
        PK,
        valor,
    )