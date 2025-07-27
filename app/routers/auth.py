from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth import register_user, check_user, create_access_token
from app.core.database import SessionLocal

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# from DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# regist
@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# login
@router.post("/login")
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    user = check_user(db, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account or Password is error."
        )
    token = create_access_token({"sub":user.username})
    return {"access_token":token, "token_type":"bearer"}

