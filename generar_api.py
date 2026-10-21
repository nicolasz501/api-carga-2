
from pathlib import Path

BASE = Path("api-reportes-ambientales")

# Tablas y columnas de la base de datos Neon.
TABLAS = {
    "roles": {
        "pk": "rol_id",
        "columnas": {
            "rol_id": "int",
            "nombre_rol": "str",
            "descripcion": "str",
            "estado": "bool",
            "fecha_creacion": "datetime",
        },
    },
    "usuarios": {
        "pk": "usuario_id",
        "columnas": {
            "usuario_id": "int",
            "rol_id": "int",
            "nombres": "str",
            "apellidos": "str",
            "correo": "str",
            "contrasena_hash": "str",
            "telefono": "str",
            "documento": "str",
            "estado": "bool",
            "fecha_creacion": "datetime",
            "fecha_actualizacion": "datetime",
        },
    },
    "modulos": {
        "pk": "modulo_id",
        "columnas": {
            "modulo_id": "int",
            "nombre_modulo": "str",
            "descripcion": "str",
            "ruta": "str",
            "icono": "str",
            "estado": "bool",
            "fecha_creacion": "datetime",
        },
    },
    "modulos_por_rol": {
        "pk": "modulo_rol_id",
        "columnas": {
            "modulo_rol_id": "int",
            "rol_id": "int",
            "modulo_id": "int",
            "puede_ver": "bool",
            "puede_crear": "bool",
            "puede_editar": "bool",
            "puede_eliminar": "bool",
            "estado": "bool",
        },
    },
    "zonas": {
        "pk": "zona_id",
        "columnas": {
            "zona_id": "int",
            "nombre_zona": "str",
            "descripcion": "str",
            "referencia": "str",
            "latitud": "float",
            "longitud": "float",
            "estado": "bool",
        },
    },
    "categorias_incidente": {
        "pk": "categoria_id",
        "columnas": {
            "categoria_id": "int",
            "nombre_categoria": "str",
            "descripcion": "str",
            "estado": "bool",
            "fecha_creacion": "datetime",
        },
    },
    "estados_reporte": {
        "pk": "estado_reporte_id",
        "columnas": {
            "estado_reporte_id": "int",
            "nombre_estado": "str",
            "descripcion": "str",
            "estado": "bool",
        },
    },
    "reportes_ambientales": {
        "pk": "reporte_id",
        "columnas": {
            "reporte_id": "int",
            "usuario_id": "int",
            "categoria_id": "int",
            "zona_id": "int",
            "estado_reporte_id": "int",
            "titulo": "str",
            "descripcion": "str",
            "direccion_referencia": "str",
            "latitud": "float",
            "longitud": "float",
            "fecha_incidente": "datetime",
            "fecha_reporte": "datetime",
            "fecha_actualizacion": "datetime",
        },
    },
    "evidencias_reporte": {
        "pk": "evidencia_id",
        "columnas": {
            "evidencia_id": "int",
            "reporte_id": "int",
            "url_archivo": "str",
            "nombre_archivo": "str",
            "tipo_archivo": "str",
            "fecha_subida": "datetime",
        },
    },
    "historial_reportes": {
        "pk": "historial_id",
        "columnas": {
            "historial_id": "int",
            "reporte_id": "int",
            "usuario_id": "int",
            "estado_anterior_id": "int",
            "estado_nuevo_id": "int",
            "observacion": "str",
            "fecha_cambio": "datetime",
        },
    },
    "comentarios_reporte": {
        "pk": "comentario_id",
        "columnas": {
            "comentario_id": "int",
            "reporte_id": "int",
            "usuario_id": "int",
            "comentario": "str",
            "fecha_comentario": "datetime",
            "estado": "bool",
        },
    },
    "validaciones_reporte": {
        "pk": "validacion_id",
        "columnas": {
            "validacion_id": "int",
            "reporte_id": "int",
            "revisor_id": "int",
            "resultado": "str",
            "observacion": "str",
            "fecha_validacion": "datetime",
        },
    },
    "notificaciones": {
        "pk": "notificacion_id",
        "columnas": {
            "notificacion_id": "int",
            "usuario_id": "int",
            "reporte_id": "int",
            "titulo": "str",
            "mensaje": "str",
            "leida": "bool",
            "fecha_creacion": "datetime",
            "fecha_lectura": "datetime",
        },
    },
}

for carpeta in (
    "database",
    "models",
    "repositories",
    "routers",
):
    (BASE / carpeta).mkdir(parents=True, exist_ok=True)

def escribir(ruta, contenido):
    destino = BASE / ruta
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido.strip() + "\n", encoding="utf-8")

# Inicializadores de paquetes
for carpeta in ("models", "repositories", "routers", "database"):
    escribir(f"{carpeta}/__init__.py", "")

escribir("database/conexion.py", r'''
import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("Falta configurar DATABASE_URL en el archivo .env")

@contextmanager
def obtener_conexion():
    conexion = psycopg2.connect(
        DATABASE_URL,
        cursor_factory=RealDictCursor,
        connect_timeout=15,
    )
    try:
        yield conexion
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
''')

escribir("database/base.py", r'''
from database.conexion import obtener_conexion

__all__ = ["obtener_conexion"]
''')

# Repositorio CRUD común.
escribir("repositories/base.py", r'''
from psycopg2 import sql
from database.conexion import obtener_conexion

def listar(tabla, limite=100, desplazamiento=0):
    consulta = sql.SQL(
        "SELECT * FROM {} ORDER BY 1 LIMIT %s OFFSET %s"
    ).format(sql.Identifier(tabla))

    with obtener_conexion() as conn:
        with conn.cursor() as cur:
            cur.execute(consulta, (limite, desplazamiento))
            return [dict(fila) for fila in cur.fetchall()]

def obtener_por_id(tabla, pk, valor):
    consulta = sql.SQL(
        "SELECT * FROM {} WHERE {} = %s"
    ).format(sql.Identifier(tabla), sql.Identifier(pk))

    with obtener_conexion() as conn:
        with conn.cursor() as cur:
            cur.execute(consulta, (valor,))
            fila = cur.fetchone()
            return dict(fila) if fila else None

def crear(tabla, datos, permitidas):
    datos = {k: v for k, v in datos.items() if k in permitidas}

    if not datos:
        raise ValueError("Debes enviar campos para crear el registro")

    columnas = list(datos.keys())
    consulta = sql.SQL(
        "INSERT INTO {} ({}) VALUES ({}) RETURNING *"
    ).format(
        sql.Identifier(tabla),
        sql.SQL(", ").join(map(sql.Identifier, columnas)),
        sql.SQL(", ").join(sql.Placeholder() for _ in columnas),
    )

    with obtener_conexion() as conn:
        with conn.cursor() as cur:
            cur.execute(consulta, list(datos.values()))
            return dict(cur.fetchone())

def actualizar(tabla, pk, valor, datos, permitidas):
    datos = {
        k: v for k, v in datos.items()
        if k in permitidas and k != pk
    }

    if not datos:
        return obtener_por_id(tabla, pk, valor)

    asignaciones = sql.SQL(", ").join(
        sql.SQL("{} = %s").format(sql.Identifier(k))
        for k in datos
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
            cur.execute(consulta, [*datos.values(), valor])
            fila = cur.fetchone()
            return dict(fila) if fila else None

def eliminar(tabla, pk, valor):
    consulta = sql.SQL(
        "DELETE FROM {} WHERE {} = %s RETURNING *"
    ).format(sql.Identifier(tabla), sql.Identifier(pk))

    with obtener_conexion() as conn:
        with conn.cursor() as cur:
            cur.execute(consulta, (valor,))
            fila = cur.fetchone()
            return dict(fila) if fila else None
''')

# Generar modelos, repositorios y routers por tabla.
for tabla, config in TABLAS.items():
    nombre = "".join(p.capitalize() for p in tabla.split("_"))
    pk = config["pk"]
    columnas = config["columnas"]

    # Esquemas Pydantic.
    campos = []
    for campo, tipo in columnas.items():
        if campo == pk:
            continue
        anotacion = {
            "int": "int",
            "str": "str",
            "bool": "bool",
            "float": "float",
            "datetime": "datetime",
        }[tipo]
        campos.append(f"    {campo}: {anotacion} | None = None")

    modelo = f'''
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class {nombre}Base(BaseModel):
    model_config = ConfigDict(extra="forbid")
{chr(10).join(campos) if campos else "    pass"}

class {nombre}Crear({nombre}Base):
    pass

class {nombre}Actualizar({nombre}Base):
    pass
'''
    escribir(f"models/{tabla}.py", modelo)

    permitidas = [c for c in columnas if c != pk]
    # En tablas con campos generados por la base de datos, se filtran
    # esos campos desde el endpoint al construir el cuerpo de entrada.
    repo = f'''
from repositories import base

TABLA = {tabla!r}
PK = {pk!r}
COLUMNAS = {permitidas!r}

def listar_registros(limite=100, desplazamiento=0):
    return base.listar(TABLA, limite, desplazamiento)

def obtener_registro(valor):
    return base.obtener_por_id(TABLA, PK, valor)

def crear_registro(datos):
    return base.crear(TABLA, datos, COLUMNAS)

def actualizar_registro(valor, datos):
    return base.actualizar(TABLA, PK, valor, datos, COLUMNAS)

def eliminar_registro(valor):
    return base.eliminar(TABLA, PK, valor)
'''
    escribir(f"repositories/{tabla}.py", repo)

    router = f'''
from fastapi import APIRouter, HTTPException, Query
from repositories import {tabla} as repo
from models.{tabla} import {nombre}Crear, {nombre}Actualizar

router = APIRouter(prefix="/{tabla.replace('_', '-')}", tags=[{tabla!r}])

@router.get("/")
def listar(
    limite: int = Query(100, ge=1, le=500),
    desplazamiento: int = Query(0, ge=0),
):
    return repo.listar_registros(limite, desplazamiento)

@router.get("/{{registro_id}}")
def obtener(registro_id: int):
    fila = repo.obtener_registro(registro_id)
    if fila is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return fila

@router.post("/", status_code=201)
def crear(datos: {nombre}Crear):
    try:
        return repo.crear_registro(datos.model_dump(exclude_unset=True))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="No se pudo crear el registro")

@router.put("/{{registro_id}}")
def actualizar(registro_id: int, datos: {nombre}Actualizar):
    fila = repo.actualizar_registro(
        registro_id, datos.model_dump(exclude_unset=True)
    )
    if fila is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return fila

@router.delete("/{{registro_id}}")
def eliminar(registro_id: int):
    fila = repo.eliminar_registro(registro_id)
    if fila is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {{"mensaje": "Registro eliminado", "registro": fila}}
'''
    escribir(f"routers/{tabla}.py", router)

imports = "\n".join(
    f"from routers.{tabla} import router as {tabla}_router"
    for tabla in TABLAS
)
incluye = "\n".join(
    f"app.include_router({tabla}_router, prefix='/api')"
    for tabla in TABLAS
)

escribir("main.py", f'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
{imports}

app = FastAPI(
    title="API de Reportes Ambientales",
    description="Sistema ciudadano de monitoreo ambiental de la Ciénaga de Mallorquín",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def inicio():
    return {{
        "mensaje": "API de reportes ambientales funcionando",
        "documentacion": "/docs",
    }}

{incluye}
''')

escribir(".env.example", '''
# Copia este archivo como .env y pega tu cadena de conexión de Neon.
DATABASE_URL=postgresql://USUARIO:CONTRASENA@HOST/BASE?sslmode=require
''')

escribir("requirements.txt", '''
fastapi
uvicorn[standard]
psycopg2-binary
python-dotenv
pydantic
''')

escribir(".gitignore", '''
.env
venv/
__pycache__/
*.pyc
''')

print(f"API generada correctamente en: {BASE.resolve()}")
print(f"Tablas incluidas: {len(TABLAS)}")
print("Configura el .env y ejecuta: uvicorn main:app --reload")
