from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import setting

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, setting.JWT_SECRET_KEY, algorithm=setting.JWT_ALGO)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=setting.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp":expire})
    return jwt.decode(to_encode, setting.JWT_SECRET_KEY, algorithms=setting.JWT_ALGO)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, setting.JWT_SECRET_KEY, algorithms=[setting.JWT_ALGO])
        return payload
    except JWTError:
        return None




