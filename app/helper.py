import re
from . import models, schemas

def is_valid_number(phone_number):
    pattern = re.compile(r'^\d{3}-\d{3}-\d{4}$')
    return bool(pattern.match(phone_number))


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