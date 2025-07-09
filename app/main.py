from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from .db import engine, Base
from .routes import create_user, get_user, update_user, delete_user
from . import auth
from sqlalchemy.orm import Session
from .db import get_db
from .models import User  
from .auth import get_current_user

Base.metadata.create_all(bind=engine)

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin"

app = FastAPI(title="User CRUD API")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Hardcoded test user
    if form_data.username == ADMIN_EMAIL and form_data.password == ADMIN_PASSWORD:
        access_token = auth.create_access_token(data={"sub": ADMIN_EMAIL})
        return {"access_token": access_token, "token_type": "bearer"}
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


app.include_router(create_user.router, prefix="/users", tags=["Users"])
app.include_router(get_user.router, prefix="/users", tags=["Users"])
app.include_router(update_user.router, prefix="/users", tags=["Users"])
app.include_router(delete_user.router, prefix="/users", tags=["Users"])
