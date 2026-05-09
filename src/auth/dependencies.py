from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.usuario import Usuario
from src.auth.security import verify_token

# Esquema de seguridad (Bearer token)
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Verifica el token JWT y retorna el usuario autenticado
    """
    token = credentials.credentials
    
    # Verificar token
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    # Obtener usuario_id del payload
    usuario_id = payload.get("sub")
    if usuario_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    # Buscar usuario en BD
    usuario = db.query(Usuario).filter(Usuario.usuario_id == int(usuario_id)).first()
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    return usuario

# 
# SOLO COPIE Y PEGUE ESTE CODIGO
# Debo arrancar desde la ultima respuesta de claude:  
# PASO F: Usar autenticación en rutas
#
