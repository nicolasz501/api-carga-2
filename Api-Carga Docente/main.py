
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import roles
from app.api import modulos
from app.api import modulos_rol
from app.api import facultades
from app.api import usuarios
from app.api import periodos_academicos
from app.api import programas_academicos
from app.api import asignaturas
from app.api import grupos
from app.api import carga_docente
from app.api import horarios
from app.api import evaluaciones
from app.api import preguntas
from app.api import respuestas


# =====================================================
# CONFIGURACIÓN PRINCIPAL DE LA API
# =====================================================

app = FastAPI(
    title="API Carga Docente",
    description=(
        "Backend modular para la gestión de carga docente, "
        "estructura académica y evaluación del desempeño "
        "utilizando FastAPI y PostgreSQL."
    ),
    version="1.0.0"
)


# =====================================================
# CONFIGURACIÓN CORS
# Permite solicitudes desde el frontend SvelteKit.
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# REGISTRO DE RUTAS
# =====================================================

app.include_router(roles.router)
app.include_router(modulos.router)
app.include_router(modulos_rol.router)
app.include_router(facultades.router)
app.include_router(usuarios.router)
app.include_router(periodos_academicos.router)
app.include_router(programas_academicos.router)
app.include_router(asignaturas.router)
app.include_router(grupos.router)
app.include_router(carga_docente.router)
app.include_router(horarios.router)
app.include_router(evaluaciones.router)
app.include_router(preguntas.router)
app.include_router(respuestas.router)


# =====================================================
# RUTA PRINCIPAL
# =====================================================

@app.get("/")
def estado_api():
    return {
        "mensaje": "La API de Carga Docente se encuentra en línea y funcional",
        "estado": "activo",
        "version": "1.0.0"
    }
