
# http://localhost:8000

# http://127.0.0.1:8000

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import List


app = FastAPI()

# Tag
class Tag(BaseModel):
    name: str
    color: str
    members: list

# Contact
class Contact(BaseModel):
    first_name: str
    last_name: str
    image: str
    phone_number: int
    reminder: int
    tags: list

@app.get("/") # decorator | Should this be login
def root():
    return {"message": "Hey Guy"}

# Read Contact
@app.get("/contact")
def get_contact():
    return {"message": "Retrieving Contact"}

# Creating Contact
@app.post("/contact")
def create_contact(new_contact: Contact):
    print(new_contact)
    return {"Contact": "Created new Contact"}

# Read Tag
@app.get("/tag")
def get_tag():
    return {"message": "Retrieving Tag"}

# Creating Tag
@app.post("/tag")
def create_tag(new_tag: Tag):
    print(new_tag)
    return {"Tag": "Created new Tag"}