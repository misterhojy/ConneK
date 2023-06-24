
# http://localhost:8000/

# http://127.0.0.1:8000/docs

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    phone_number: str # unique
    user_id: int


class Contact(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    since_last: int

@app.get("/") # decorator
def root():
    return {"message": "Hello World"}

# Contacts

# Create a contact


# Read ONE contact

@app.get("/contacts")
def get_contact():
    pass

# Read ALL contacts



# Update a contact



# Delete a contact


# Login -> Click contact -> Send Hangout Request with message and date -> Request object gets created (Request: Title (hung out at starbucks), Message (todayu was a greate day got venti sometig) (saved to the journal), Date, Button)


# Login -> Click contact -> Send Hangout Request with message "coffe tm?" and date ->Hangout Request object gets created (Request: Contact name , Message (coffe tm?) (saved to the journal), Date, Button) -> 
# hung out, resets timer Notes object (saved to journal) "had coffe with friend talked ab plans" button

# Login -> Click contact -> Send Hangout Request with message "coffe tm?" and date -> Save a message AND send a message, ALSO create FORM (form: title, message, date, button)

# Sender_Request: (Title, Body, Date of Plan) -> # iMessage == Sender_Request (Messaging API) AND ()



# Login

# Users: username, number (CRUD)

# Contact: (username, number) -> Users, since-last-count (CRUD)

# Group: collection of Contact.obj, since-last-count (CRUD)

# Tags: name, collection of contact.obj (CRUD)

# Journal: title, message body, date