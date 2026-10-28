from pydantic import BaseModel, EmailStr 
from datetime import datetime
from typing import Optional

class TodoCreate(BaseModel):
    title: str
    description: str
    completed: Optional[bool] = False 

class TodoResponse(TodoCreate):
    id: int
    created_at: datetime
    owner_id : int
    
    class Config:
            from_attributes = True
    

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
            from_attributes = True

class UserLogin(BaseModel):
     email : EmailStr
     password : str

     class Config:
                 from_attributes = True

class Token(BaseModel):
      access_token : str
      token_type : str

class TokenData(BaseModel):
      id: Optional[int | str] = None