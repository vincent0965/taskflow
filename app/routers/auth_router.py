from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import verify_pw, create_access_token, get_pw_hash
from app.models.user import User
from app.schemas.user import UserLogin, UserCreate

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


