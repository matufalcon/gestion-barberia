from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.usuario import Usuario
from src.schemas.auth import LoginRequest, TokenResponse
from src.auth.security import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario por email
    usuario = db.query(Usuario).filter(Usuario.email == credentials.email).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Verificar contraseña
    if not verify_password(credentials.password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Crear token JWT
    access_token = create_access_token(data={"sub": str(usuario.usuario_id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }