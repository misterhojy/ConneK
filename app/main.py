
# http://localhost:8000

# http://127.0.0.1:8000

from fastapi import FastAPI, status, HTTPException, Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
def create_contact(contact: schemas.Contact, db: Session = Depends(get_db)):

    # NOT USING SQLALCHEMY
    #cursor.execute("""INSERT INTO contacts ("first name", "last name", "phone number", "image", "reminder") VALUES
    #                (%s, %s, %s, %s, %s) RETURNING *""", (contact.first_name, contact.last_name, contact.phone_number, contact.image, contact.reminder))
    #new_contact = cursor.fetchone()
    #connection.commit()

    new_contact = models.Contact(**contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return {"data": new_contact}



# Read Contacts
@app.get("/contacts")
def get_contacts(db: Session = Depends(get_db)):

    contacts = db.query(models.Contact).all()
    return {"data": contacts}



# Read One Contact
@app.get("/contacts/{id}")
def get_contact(id: int, db: Session = Depends(get_db)):

    #cursor.execute("""SELECT * FROM contacts WHERE id = %s""", (str(id),))
    
    contact = db.query(models.Contact).filter(models.Contact.id == id).first()

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")
    
    return {"data": contact}



# Updating Contact
@app.put("/contacts/{id}")
def update_contact(id: int, contact: schemas.Contact, db: Session = Depends(get_db)):

    contact_query = db.query(models.Contact).filter(models.Contact.id == id)
    updated_contact = contact_query.first()

    if updated_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")  
    
    contact_query.update(contact.dict(), synchronize_session=False)
    db.commit()
    return {"data": contact_query.first()}



# Deleting Contact
@app.delete("/contacts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(id: int, db: Session = Depends(get_db)):

    #cursor.execute("""DELETE FROM contacts WHERE id = %s RETURNING *""", (str(id),))

    contact = db.query(models.Contact).filter(models.Contact.id == id)

    if contact.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")
    
    contact.delete(synchronize_session=False)
    db.commit()

       

