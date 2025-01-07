from datetime import timedelta

from fastapi import APIRouter, status, HTTPException

from database import crud, schemas
from database import models
from utils import Annotations
from utils.jwt_handler import create_access_token

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_user(db: Annotations.db_dependency, user_create: schemas.UserCreate):
    return crud.create_user(db, user_create)


@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Annotations.db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user



@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotations.form_data,
                                 db: Annotations.db_dependency):
    user = crud.authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.email, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}