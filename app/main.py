from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas , utils
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API - SQLAlchemy ORM Version")

@app.post("/todos/", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    new_todo = models.Todo(**todo.model_dump()) 
    db.add(new_todo)     
    db.commit()         
    db.refresh(new_todo) 
    return new_todo

@app.get("/todos/", response_model=List[schemas.TodoResponse])
async def read_todos(db: Session = Depends(get_db)):
    all_todos = db.query(models.Todo).all()
    return all_todos

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_query = db.query(models.Todo).filter(models.Todo.id == todo_id)
    todo = todo_query.first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id: {todo_id} does not exist")
    todo_query.delete(synchronize_session=False)
    db.commit()
    return None


@app.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
async def update_todo(todo_id: int, updated_todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    todo_query = db.query(models.Todo).filter(models.Todo.id == todo_id)
    todo = todo_query.first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id: {todo_id} does not exist")
    todo_query.update(updated_todo.model_dump(), synchronize_session=False)
    db.commit()
    return todo_query.first()

@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.model_dump())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user