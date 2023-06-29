
# http://localhost:8000

# http://127.0.0.1:8000

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# Tag
class Tag(BaseModel):
    name: str
    color: Optional[str] = None
    members: Optional[list] = None


# Contact
class Contact(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    image: Optional[str] = None
    phone_number: Optional[int] = None
    reminder: Optional[int] = None
    tags: Optional[list] = None


# Creating new tags
gym_tag = Tag(name="Gym")
basketball_tag = Tag(name="Basketball")

my_contacts = [{ "first_name": "Hojat", "last_name": "Jaffary", "image": "/path/to/image/file", "phone_number": "6314647797", "reminder": 7, "tags": [], "id": 1}, 
                { "first_name": "Sahail", "last_name": "Jaffary", "phone_number": "6315699178", "id": 2},
                { "first_name": "Mason", "last_name": "Taylor", "phone_number": "6318001686", "reminder": 3, "tags": [gym_tag, basketball_tag], "id": 3}]

def find_contact(id):
    contact = None
    for c in my_contacts:
        if c.get('id') == id:
            contact = c
            return contact
    return contact


@app.get("/") # decorator | Should this be login
def root():
    return {"message": "Hey Guy"}


# Read Contacts
@app.get("/contacts")
def get_contacts():
    return {"data": my_contacts}


# Read One Contact
@app.get("/contacts/{id}")
def get_contact(id: int):
    # Need to find id in array of contacts
    contact = find_contact(id)
    if contact:
        return {"data": contact}
    else:
        return {"message": "Contact not found"}


# Creating Contact
@app.post("/contacts")
def create_contact(contact: Contact):
    contact_dict = contact.dict()
    contact_dict['id'] = randrange(0, 1000000)
    my_contacts.append(contact_dict)
    return {"data": contact_dict}



# Read Tag
@app.get("/tags")
def get_tags():
    return {"message": "Retrieving Tag"}


# Creating Tag
@app.post("/tags")
def create_tag(new_tag: Tag):
    print(new_tag)
    return {"Tag": "Created new Tag"}