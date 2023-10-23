from datetime import datetime
from pydantic import BaseModel, validator
from typing import Optional


# Contact
class ContactBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    phone_number: Optional[int] = None  # Make Sure it is a valid number
    image: Optional[str] = None
    reminder: Optional[int] = None

class UpdateContact(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[int] = None 
    image: Optional[str] = None
    reminder: Optional[int] = None

class CreateContact(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int
    since_last_hangout: int
    # created_at NOT WORKING??

    class Config:
        from_attributes = True

# User
#class CreateUser(BaseModel):
#    phone_number: int   # Make Sure it is a valid number
#    password: str
#
#    @validator('phone_number')
#    def validate_phone_number(cls, phone_number):
#        
#        # validation: Phone number must be a positive integer
#        if phone_number <= 0:
#            raise ValueError("Phone number must be a positive integer")
#        
#        # validation: Phone number
#        
#        return phone_number
