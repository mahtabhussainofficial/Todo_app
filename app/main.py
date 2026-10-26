from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas , utils 
from app.database import engine, get_db
from .routes import todos, user , auth
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API - SQLAlchemy ORM Version")


app.include_router(todos.router)
app.include_router(user.router)
app.include_router(auth.router)