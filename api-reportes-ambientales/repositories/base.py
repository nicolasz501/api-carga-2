
from psycopg2 import sql

from database.conexion import obtener_conexion


def _validar_identificador(nombre, descripcion="identificador"):
    """Valida que los nombres de tablas y columnas sean cadenas válidas."""
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError(f"El {descripcion} no es válido")

    return nombre


def listar(tabla, limite=100, desplazamiento=0):
    """Lista registros con paginación."""
    _validar_identificador(tabla, "nombre de tabla")

    if not isinstance(limite, int) or not 1 <= limite <= 500:
        raise ValueError("El límite debe estar entre 1 y 500")

    if not isinstance(desplazamiento, int) or desplazamiento < 0:
        raise ValueError("El desplazamiento no puede ser negativo")

    consulta = sql.SQL(
        "SELECT * FROM {} ORDER BY 1 LIMIT %s OFFSET %s"
    ).format(sql.Identifier(tabla))

    with obtener_conexion() as conn:
        with conn.cursor() as cur:
            cur.execute(consulta, (limite, desplazamiento))
            return [dict(fila) for fila in cur.fetchall()]


def obtener_por_id(tabla, pk, valor):
    """Obtiene un registro por su clave primaria."""
    _validar_identificador(tabla, "nombre de tabla")
    _validar_identificador(pk, "nombre de clave primaria")

    consulta = sql.SQL(
        "SELECT * FROM {} WHERE {} = %s"
    ).format(
        sql.Identifier(tabla),
        sql.Identifier(pk),
    )

    with obtener_conexion() as conn:
        with conn.cursor() as cur:
            cur.execute(consulta, (valor,))
            fila = cur.fetchone()

            return dict(fila) if fila is not None else None


def crear(tabla, datos, permitidas):
    """Inserta un registro usando exclusivamente columnas permitidas."""
    _validar_identificador(tabla, "nombre de tabla")

    if not isinstance(datos, dict):
        raise ValueError("Los datos deben enviarse como un objeto")

    permitidas = set(permitidas)

    # Rechazar campos desconocidos en lugar de descartarlos silenciosamente.
    desconocidas = set(datos.keys()) - permitidas

    if desconocidas:
        raise ValueError(
            "Campos no permitidos: " + ", ".join(sorted(desconocidas))
        )

    if not datos:
        raise ValueError("Debes enviar campos para crear el registro")

    columnas = list(datos.keys())

    for columna in columnas:
        _validar_identificador(columna, "nombre de columna")

    consulta = sql.SQL(
        "INSERT INTO {} ({}) VALUES ({}) RETURNING *"
    ).format(
        sql.Identifier(tabla),
        sql.SQL(", ").join(
            sql.Identifier(columna) for columna in columnas
        ),
        sql.SQL(", ").join(
            sql.Placeholder() for _ in columnas
        ),
    )

    with obtener_conexion() as conn:
        with conn.cursor() as cur:
            cur.execute(consulta, list(datos.values()))
            fila = cur.fetchone()

            if fila is None:
                raise RuntimeError("No se pudo recuperar el registro creado")

            return dict(fila)


def actualizar(tabla, pk, valor, datos, permitidas):
    """Actualiza un registro mediante su clave primaria."""
    _validar_identificador(tabla, "nombre de tabla")
    _validar_identificador(pk, "nombre de clave primaria")

    if not isinstance(datos, dict):
        raise ValueError("Los datos deben enviarse como un objeto")

    permitidas = set(permitidas)

    # La clave primaria nunca se modifica desde esta función.
    desconocidas = set(datos.keys()) - permitidas

    if desconocidas:
        raise ValueError(
            "Campos no permitidos: " + ", ".join(sorted(desconocidas))
        )

    datos = {
        columna: valor_nuevo
        for columna, valor_nuevo in datos.items()
        if columna != pk
    }

    if not datos:
        return obtener_por_id(tabla, pk, valor)

    for columna in datos:
        _validar_identificador(columna, "nombre de columna")

    asignaciones = sql.SQL(", ").join(
        sql.SQL("{} = %s").format(sql.Identifier(columna))
        for columna in datos
    )

    consulta = sql.SQL(
        "UPDATE {} SET {} WHERE {} = %s RETURNING *"
    ).format(
        sql.Identifier(tabla),
        asignaciones,
        sql.Identifier(pk),
    )

    with obtener_conexion() as conn:
        with conn.cursor() as cur:
            cur.execute(
                consulta,
                [*datos.values(), valor],
            )

            fila = cur.fetchone()
            return dict(fila) if fila is not None else None


def eliminar(tabla, pk, valor):
    """Elimina un registro por su clave primaria."""
    _validar_identificador(tabla, "nombre de tabla")
    _validar_identificador(pk, "nombre de clave primaria")

    consulta = sql.SQL(
        "DELETE FROM {} WHERE {} = %s RETURNING *"
    ).format(
        sql.Identifier(tabla),
        sql.Identifier(pk),
    )

    with obtener_conexion() as conn:
        with conn.cursor() as cur:
            cur.execute(consulta, (valor,))
            fila = cur.fetchone()

            return dict(fila) if fila is not None else None
