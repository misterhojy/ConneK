import re
from fastapi import HTTPException, status
from . import models, schemas


def is_valid_number(phone_number):
    pattern = re.compile(r'^\d{3}-\d{3}-\d{4}$')
    result = bool(pattern.match(phone_number))
    if result is not True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Phone Number: {phone_number}")


#SQL Alchemy model into Pydantic model function
def create_contactResponse(contact: models.Contact):
    contact_response = schemas.ContactResponse(
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

def update_attributes(contact: models.Contact):
    attribute_updates = {}

    if contact.first_name:
        attribute_updates["first_name"] = contact.first_name
    if contact.last_name:
        attribute_updates["last_name"] = contact.last_name
    if contact.phone_number:
        attribute_updates["phone_number"] = contact.phone_number
    if contact.reminder:
        attribute_updates["reminder"] = contact.reminder
    if contact.image:
        attribute_updates["image"] = contact.image

    return attribute_updates