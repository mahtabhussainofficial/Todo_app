
from fastapi import FastAPI, Depends, HTTPException, status ,APIRouter
from sqlalchemy.orm import Session
from .. import models , schemas , auth2
from ..database import get_db
from typing import List


router = APIRouter(
    prefix= "/todos",
    tags=['todos'],
)

@router.post("/", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: schemas.TodoCreate, 
    db: Session = Depends(get_db), 
    current_user: schemas.TokenData = Depends(auth2.get_current_user)
):
    new_todo = models.Todo(owner_id = current_user.id , **todo.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/", response_model=List[schemas.TodoResponse])
async def read_todos(
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(auth2.get_current_user)
):
    all_todos = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id).all()
    return all_todos

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(auth2.get_current_user)
):
    todo_query = db.query(models.Todo).filter(models.Todo.id == todo_id)
    todo = todo_query.first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id: {todo_id} does not exist")
    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="not authorized to perform this action.") 
    todo_query.delete(synchronize_session=False)
    db.commit()
    return None


@router.put("/{todo_id}", response_model=schemas.TodoResponse)
async def update_todo(
    todo_id: int,
    updated_todo: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(auth2.get_current_user)
):
    todo_query = db.query(models.Todo).filter(models.Todo.id == todo_id)
    todo = todo_query.first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id: {todo_id} does not exist")
    if todo.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Not authorized to perform requested action"
        )
    todo_query.update(updated_todo.model_dump(), synchronize_session=False)
    db.commit()
    return todo_query.first()

@router.get("/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(auth2.get_current_user)
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Todo with id: {todo_id} does not exist"
        )
    if todo.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    return todo