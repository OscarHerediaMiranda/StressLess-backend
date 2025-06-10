from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from config import SECRET_KEY, ALGORITHM
from fastapi.security import APIKeyHeader
oauth2_scheme = APIKeyHeader(name="Authorization")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)):
    print("🔐 TOKEN RECIBIDO:", token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token no válido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 🔧 Remueve "Bearer " si está presente
        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM) 
        print("✅ Payload decodificado:", payload)

        correo: str = payload.get("sub")
        rol: str = payload.get("rol")

        if correo is None or rol is None:
            raise credentials_exception

        return {"correo": correo, "rol": rol}
    except JWTError:
        raise credentials_exception
        