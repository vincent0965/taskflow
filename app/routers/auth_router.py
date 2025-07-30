from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import verify_pw, create_access_token, get_pw_hash
from app.models.user import User
from app.schemas.user import UserLogin, UserCreate
from app.config import setting
from app.utils import create_access_token
from datetime import timedelta
from jose import jwt, JWTError


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# regist
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pw = get_pw_hash(user.pw)
    new_user = User(username=user.username, email=user.email, hash_pw=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg":"User registered successful"}


# login
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_pw(user.pw, db_user.hash_pw):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type":"bearer"}


# refresh_token
@router.post("/refresh")
def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, setting.JWT_SECRET_KEY, algorithms=[setting.JWT_ALGO])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    print(f"Generated Access Token: {new_access_token}")

    return {
        "access_token":new_access_token,
        "token_type":"bearer"
    }

