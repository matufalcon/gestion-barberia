from pydantic import BaseModel

#schema para login
class LoginRequest(BaseModel):
    email: str
    password: str

#schema para respuesta del login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"