from datetime import datetime, timedelta
from jose import JWTError, jwt 
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

#configuracion
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

#contexto para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#hashear contraseña 
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


#verificar contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#crear token jwt
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#verificar token jwt
def verify_token(token: str) -> dict:
    try:
        playload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return playload
    except JWTError:
        return None