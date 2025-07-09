from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import is_self_or_admin
from app.db import get_db
from app.models import User


router = APIRouter()
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(is_self_or_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": f"User {user.email} deleted"}
