
import os
from contextlib import contextmanager
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


# Ruta raíz del proyecto, suponiendo que este archivo está en database/
BASE_DIR = Path(__file__).resolve().parent.parent

# Carga el .env ubicado en la raíz del proyecto.
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError(
        "Falta configurar DATABASE_URL en el archivo .env "
        "ubicado en la raíz del proyecto"
    )


@contextmanager
def obtener_conexion():
    conexion = None

    try:
        conexion = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=RealDictCursor,
            connect_timeout=15,
        )

        yield conexion

        # Confirma los cambios si no hubo excepciones.
        conexion.commit()

    except Exception:
        # Revierte los cambios si la conexión llegó a abrirse.
        if conexion is not None:
            conexion.rollback()
        raise

    finally:
        # Cierra la conexión incluso si ocurre un error.
        if conexion is not None:
            conexion.close()
