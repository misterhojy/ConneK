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


# Get User NOT NEEDED MAYBE
#@router.get("/users/{id}", response_model=schemas.UserResponse)
#def get_user(id: int, db: Session = Depends(get_db)):
#    
#    user = db.query(models.Contact).filter(models.User.user_id == id).first()
#
#    if user is None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id of {id} not found")
#    
#    return user