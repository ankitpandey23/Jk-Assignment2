from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.auth import is_self_or_admin
from app.db import get_db
from app.models import User

router = APIRouter()

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

@router.patch("/{user_id}")
def update_user(
    user_id: int,
    fields: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda: is_self_or_admin(user_id))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in fields.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
