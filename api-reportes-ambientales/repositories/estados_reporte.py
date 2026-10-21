
from repositories import base

TABLA = "estados_reporte"
PK = "estado_reporte_id"

COLUMNAS = [
    "nombre_estado",
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


def obtener_por_nombre(nombre_estado):
    estados = base.listar(
        TABLA,
        limite=500,
        desplazamiento=0,
    )

    nombre_buscado = nombre_estado.strip().casefold()

    for estado in estados:
        nombre = str(estado.get("nombre_estado", "")).strip().casefold()

        if nombre == nombre_buscado and estado.get("estado") is True:
            return estado

    return None


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
