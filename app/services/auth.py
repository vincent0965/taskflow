from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils import create_access_token
from app.config import setting

import os

# hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# eviroment parameter
secret_key = os.getenv("SECRET_KEY")
algo = os.getenv("ALGORITHM")
access_token = int(os.getenv("ACCESS_TOKEN", 30))

# pw cover
def hash_pw(pw: str) -> str:
    return pwd_context.hash(pw)

# pw check
def verify_pw(plain_pw: str, hashed_pw: str) -> bool:
    return pwd_context.verify(plain_pw, hashed_pw)

# jwt token
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=access_token)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algo)

# regist user
def register_user(db: Session, user_data: UserCreate):

    existing_user = db.query(User).filter(User.username == user_data.username).first()

    if existing_user:
        raise ValueError("This User had.")
    
    hashed_pw = hash_pw(user_data.pw)
    new_user = User(
        username = user_data.username,
        email = user_data.email,
        hash_pw = hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# login check
def check_user(db: Session, user_data: UserLogin):

    user = db.query(User).filter(User.username == user_data.username).first()

    if not user or not verify_pw(user_data.pw, user.hash_pw):
        return None
    
    return user

# login
def login(user_data: UserLogin):
    access_token_expires = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=setting.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(data={"sub":user_data.username}, expires_delta=access_token_expires)
    refresh_token = create_access_token(data={"sub":user_data.username}, expires_delta=refresh_token_expires)

    return{
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
    }




