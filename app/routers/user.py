from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from .. import models, schemas, helper, oauth2
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=['Users']
)
# USER
# Create User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_contact(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hash password, user.password
    hashed_password = helper.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Get Current User
@router.get("/", response_model=schemas.UserResponse)
def get_user(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    return current_user