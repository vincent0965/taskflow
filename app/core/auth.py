from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# jwt
SECRET_KEY = "admin"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pw_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_pw(plain_pw, hashed_pw):
    return pw_content.verify(plain_pw, hashed_pw)

def get_pw_hash(pw):
    return pw_content.hash(pw)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
