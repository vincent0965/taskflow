from pydantic import BaseModel, EmailStr

# like Java model

# register
class UserCreate(BaseModel):
    username:str
    email:EmailStr
    pw:str

# login
class UserLogin(BaseModel):
    username:str
    pw:str

# response into front end
class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr

    class Config:
        orm_model = True # let SQL model auto transfor Pydantic



