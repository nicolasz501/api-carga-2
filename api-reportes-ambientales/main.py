
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.roles import router as roles_router
from routers.usuarios import router as usuarios_router
from routers.modulos import router as modulos_router
from routers.modulos_por_rol import router as modulos_por_rol_router
from routers.zonas import router as zonas_router
from routers.categorias_incidente import router as categorias_incidente_router
from routers.estados_reporte import router as estados_reporte_router
from routers.reportes_ambientales import router as reportes_ambientales_router
from routers.evidencias_reporte import router as evidencias_reporte_router
from routers.historial_reportes import router as historial_reportes_router
from routers.comentarios_reporte import router as comentarios_reporte_router
from routers.validaciones_reporte import router as validaciones_reporte_router
from routers.notificaciones import router as notificaciones_router

app = FastAPI(
    title="API de Reportes Ambientales",
    description="Sistema ciudadano de monitoreo ambiental de la Ciénaga de Mallorquín",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://cargadocente.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def inicio():
    return {
        "status": "ok",
        "mensaje": "API de reportes ambientales funcionando",
        "documentacion": "/docs",
    }

app.include_router(roles_router, prefix="/api")
app.include_router(usuarios_router, prefix="/api")
app.include_router(modulos_router, prefix="/api")
app.include_router(modulos_por_rol_router, prefix="/api")
app.include_router(zonas_router, prefix="/api")
app.include_router(categorias_incidente_router, prefix="/api")
app.include_router(estados_reporte_router, prefix="/api")
app.include_router(reportes_ambientales_router, prefix="/api")
app.include_router(evidencias_reporte_router, prefix="/api")
app.include_router(historial_reportes_router, prefix="/api")
app.include_router(comentarios_reporte_router, prefix="/api")
app.include_router(validaciones_reporte_router, prefix="/api")
app.include_router(notificaciones_router, prefix="/api")
