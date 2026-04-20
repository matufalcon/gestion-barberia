from fastapi import FastAPI
from src.routes import usuario, servicio, barbero, turno, auth

app = FastAPI(
    title="Barbería API",
    description="Sistema de gestion para barberias",
    version="1.0.0"
)

app.include_router(usuario.router)
app.include_router(servicio.router)
app.include_router(barbero.router)
app.include_router(turno.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Barbería API - Sistema de gestion"}

@app.get("/health")
def health_check():
    return {"status": "OK"}