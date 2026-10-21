
from repositories import base
from psycopg2 import sql

from database.conexion import obtener_conexion


TABLA = "usuarios"
PK = "usuario_id"

COLUMNAS = [
    "rol_id",
    "nombres",
    "apellidos",
    "correo",
    "contrasena_hash",
    "telefono",
    "documento",
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


def obtener_por_correo(correo):
    """Busca un usuario por su correo electrónico."""
    consulta = sql.SQL(
        "SELECT * FROM {} WHERE LOWER({}) = LOWER(%s) LIMIT 1"
    ).format(
        sql.Identifier(TABLA),
        sql.Identifier("correo"),
    )

    with obtener_conexion() as conn:
        with conn.cursor() as cur:
            cur.execute(consulta, (correo.strip(),))
            fila = cur.fetchone()

            return dict(fila) if fila is not None else None


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
