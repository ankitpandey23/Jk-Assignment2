from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from .db import engine, Base
from .routes import create_user, get_user, update_user, delete_user
from . import auth
from sqlalchemy.orm import Session
from .db import get_db
from .models import User  # Adjust if your User model is elsewhere

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User CRUD API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Dependency to get current user from JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = auth.decode_access_token(token)
    if payload is None:
        raise credentials_exception
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    # Hardcoded user for testing
    if email == "admin@example.com":
        return {"email": "admin@example.com", "name": "admin"}
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Hardcoded test user
    if form_data.username == "admin@example.com" and form_data.password == "admin":
        access_token = auth.create_access_token(data={"sub": "admin@example.com"})
        return {"access_token": access_token, "token_type": "bearer"}
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Example of a protected route
@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

app.include_router(create_user.router, prefix="/users", tags=["Users"])
app.include_router(get_user.router, prefix="/users", tags=["Users"])
app.include_router(update_user.router, prefix="/users", tags=["Users"])
app.include_router(delete_user.router, prefix="/users", tags=["Users"])
