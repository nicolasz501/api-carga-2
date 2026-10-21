
from repositories import base


TABLA = "modulos_por_rol"
PK = "modulo_rol_id"

COLUMNAS = [
    "rol_id",
    "modulo_id",
    "puede_ver",
    "puede_crear",
    "puede_editar",
    "puede_eliminar",
    "estado",
]

CAMPOS_PERMISOS = (
    "puede_ver",
    "puede_crear",
    "puede_editar",
    "puede_eliminar",
)


def validar_permisos(datos):
    """Evita permisos de escritura sin permiso de visualización."""
    puede_ver = datos.get("puede_ver")

    if puede_ver is False:
        for campo in ("puede_crear", "puede_editar", "puede_eliminar"):
            if datos.get(campo) is True:
                raise ValueError(
                    f"{campo} no puede ser True cuando puede_ver es False"
                )


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
    validar_permisos(datos)

    return base.crear(
        TABLA,
        datos,
        COLUMNAS,
    )


def actualizar_registro(valor, datos):
    actual = obtener_registro(valor)

    if actual is None:
        return None

    # Combinar permisos existentes con los campos recibidos.
    permisos_finales = {
        campo: datos.get(campo, actual.get(campo))
        for campo in CAMPOS_PERMISOS
    }

    validar_permisos(permisos_finales)

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
