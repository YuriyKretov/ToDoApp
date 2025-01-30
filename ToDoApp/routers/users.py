from fastapi import APIRouter, Request, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from ToDoApp.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ToDoApp.models import Todos, Users
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix="/user",
    tags=["🤖 User"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


# @router.get("/", status_code=status.HTTP_200_OK)
# async def get_user(user: user_dependency, db: db_dependency):
#     if user is None:
#         raise HTTPException(401, "Authentication credentials were not provided.")
#
#     user_model = db.query(Users).filter(Users.id == user.get('user_id')).first()
#
#     if not user_model:
#         raise HTTPException(404, "User not found.")
#
#     return user_model

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: user_dependency,
                          db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(401, "Authentication credentials were not provided.")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(401, "Error on password change.")

    user_model.hashed_password = bcrypt_context.hash(user_verification.password)
    db.add(user_model)
    db.commit()


@router.put('/phone_number/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency,
                          db: db_dependency,
                          phone_number: str):
    if user is None:
        raise HTTPException(401, "Authentication failed")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number

    db.add(user_model)
    db.commit()