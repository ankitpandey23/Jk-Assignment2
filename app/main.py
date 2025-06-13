from fastapi import FastAPI
from .db import engine, Base
from .routes import create_user, get_user, update_user, delete_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User CRUD API")

app.include_router(create_user.router, prefix="/users", tags=["Users"])
app.include_router(get_user.router, prefix="/users", tags=["Users"])
app.include_router(update_user.router, prefix="/users", tags=["Users"])
app.include_router(delete_user.router, prefix="/users", tags=["Users"])
