from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.db import get_db
from app.models import User

router = APIRouter()

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

@router.patch("/{user_id}", response_model=UserUpdate)
def update_user(user_id: int, fields: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = fields.dict(exclude_unset=True)
    for key, val in update_data.items():
        setattr(db_user, key, val)
    db.commit()
    db.refresh(db_user)
    return db_user
