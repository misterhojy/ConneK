from pydantic import BaseModel
from typing import Optional
from . import models

# Contact
class ContactBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    image: Optional[str] = None
    reminder: Optional[int] = None

class UpdateContact(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None 
    image: Optional[str] = None
    reminder: Optional[int] = None

class ContactResponse(BaseModel):
    contact_id: int
    first_name: str
    last_name: Optional[str] = None
    days_since_last_hangout: int
    phone_number: Optional[str] = None
    image: Optional[str] = None
    reminder: Optional[int] = None
    created_at: str

#SQL Alchemy model into Pydantic model function
def create_contactResponse(contact: models.Contact):
    contact_response = ContactResponse(
        contact_id = contact.contact_id,
        first_name = contact.first_name,
        last_name = contact.last_name,
        days_since_last_hangout = contact.days_since_last_hangout(),
        phone_number = contact.phone_number,
        image = contact.image,
        reminder = contact.reminder,
        created_at = str(contact.created_at)
    )

    return contact_response