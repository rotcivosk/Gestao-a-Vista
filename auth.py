from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

# Chave secreta - Gera uma qualquer, aqui é exemplo
SECRET_KEY = "ad48e7ff3e07cb4fffc96044bbdb843272d8bb1741cb7a2f3404f459dbf2420f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hora

def criar_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = payload.get("sub")
        return str(usuario_id) if usuario_id else None
    except JWTError:
        return None
