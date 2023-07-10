
# http://localhost:8000

# http://127.0.0.1:8000

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# Tag
class Tag(BaseModel):
    name: str
    color: Optional[str] = None

# Contact
class Contact(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    phone_number: Optional[int] = None
    image: Optional[str] = None
    reminder: Optional[int] = None

# Group
class Group(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    reminder: Optional[str] = None


while True:
    try:
        connection = psycopg2.connect(host='localhost', database='Konnec-Project', user='postgres', password='7)&:Bravo79)', 
                                    cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(10)


# Creating Contact
@app.post("/contacts", status_code=status.HTTP_201_CREATED)
def create_contact(contact: Contact):
    cursor.execute("""INSERT INTO contacts ("first name", "last name", "phone number", "image", "reminder") VALUES
                    (%s, %s, %s, %s, %s) RETURNING *""", (contact.first_name, contact.last_name, contact.phone_number, contact.image, contact.reminder))
    new_contact = cursor.fetchone()
    connection.commit()
    return {"data": new_contact}


# Read Contacts
@app.get("/contacts")
def get_contacts():
    cursor.execute("""SELECT * FROM contacts """)
    contacts = cursor.fetchall()
    return {"data": contacts}


# Read One Contact
@app.get("/contacts/{id}")
def get_contact(id: int, response: Response):
    cursor.execute("""SELECT * FROM contacts WHERE id = %s""", (str(id),))
    contact = cursor.fetchone()
    if contact:
        return {"data": contact}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")
    

# Updating Contact
@app.put("/contacts/{id}")
def update_contact(id: int, contact: Contact):
    cursor.execute("""UPDATE contacts SET "first name" = %s, "last name" = %s, "phone number" = %s, "image" = %s, "reminder" = %s WHERE id = %s RETURNING *""",
                   (contact.first_name, contact.last_name, contact.phone_number, contact.image, contact.reminder, (str(id))))
    updated_contact = cursor.fetchone()
    connection.commit()
    if updated_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")    
    return {"data": updated_contact}


# Deleting Contact
@app.delete("/contacts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(id: int):
    cursor.execute("""DELETE FROM contacts WHERE id = %s RETURNING *""", (str(id),))
    deleted_contact = cursor.fetchone()
    connection.commit()
    if deleted_contact == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
       

# Read Tag
@app.get("/tags")
def get_tags():
    return {"message": "Retrieving Tag"}


# Creating Tag
@app.post("/tags")
def create_tag(new_tag: Tag):
    print(new_tag)
    return {"Tag": "Created new Tag"}