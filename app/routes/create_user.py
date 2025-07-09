from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.db import get_db
from app.models import User
from app.auth import get_current_user, get_password_hash
from app.email_sender import send_email_async


router = APIRouter()

USER_PASSWORD = "12345"  

class UserCreate(BaseModel):
    name: str
    email: EmailStr

@router.post("/create", response_model=UserCreate)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(name=user.name, email=user.email, hashed_password=get_password_hash(USER_PASSWORD))  
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    try:
        await send_email_async(user.email, "Welcome to the User Management System", f"Hello {user.name},\n\nThank you for registering with us! Your account has been created successfully. Here is your password {USER_PASSWORD}.\n\nBest regards,\nUser Management Team")
    except Exception as e:
        res = f"Failed to send email: {str(e)}"
        print(res)
    return db_user
