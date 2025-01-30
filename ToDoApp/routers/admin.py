from fastapi import APIRouter, Request, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from ToDoApp.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ToDoApp.models import Todos
from .auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["🛡️ Admin"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def get_todos(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=404, detail='Authentication Failed')
    return db.query(Todos).all()


@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency,
                      db: db_dependency, todo_id: int = Path(ge=1)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()