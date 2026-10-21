
from repositories import base


TABLA = "categorias_incidente"
PK = "categoria_id"

# Columnas que se pueden modificar desde la API.
COLUMNAS = [
    "nombre_categoria",
    "descripcion",
    "estado",
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
