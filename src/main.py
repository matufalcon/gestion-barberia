from fastapi import FastAPI
from src.routes import usuario

app = FastAPI(
    title="Barbería API",
    description="Sistema de gestion para barberias",
    version="1.0.0"
)

app.include_router(usuario.router)

@app.get("/")
def root():
    return {"message": "Barbería API - Sistema de gestion"}

@app.get("/health")
def health_check():
    return {"status": "OK"}