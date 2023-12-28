from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas
from .database import engine, get_db
from .helper import is_valid_number, create_contactResponse, update_attributes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        connection = psycopg2.connect(host='localhost', database='ConneK-Project', user='postgres', password='7)&:Bravo79)', 
                                    cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(10)


# Creating Contact
@app.post("/contacts", status_code=status.HTTP_201_CREATED, response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactBase, db: Session = Depends(get_db)):

    if contact.phone_number:
        is_valid_number(contact.phone_number)

    new_contact = models.Contact(**contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return create_contactResponse(new_contact)


# Read Contacts
@app.get("/contacts", response_model=List[schemas.ContactResponse])
def get_contacts(db: Session = Depends(get_db)):

    contacts = db.query(models.Contact).all()

    # Convert the SQLAlchemy Contact models to the Pydantic ContactResponse models
    contact_responses = [
        create_contactResponse(contact) #creating new object of ContactResponse for ever SQL model
        for contact in contacts
    ]      
    return contact_responses


# Read One Contact
@app.get("/contacts/{id}", response_model=schemas.ContactResponse)
def get_contact(id: int, db: Session = Depends(get_db)):
    
    contact = db.query(models.Contact).filter(models.Contact.contact_id == id).first()

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")
    
    return create_contactResponse(contact)


# Updating Replace Contact I DONT THINK YOU NEED THIS
@app.put("/contacts/{id}", response_model=schemas.ContactResponse)
def update_contact(id: int, contact: schemas.ContactBase, db: Session = Depends(get_db)):

    contact_query = db.query(models.Contact).filter(models.Contact.contact_id == id)
    updated_contact = contact_query.first()

    if updated_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")  

    if contact.phone_number:
        is_valid_number(contact.phone_number)
    
    contact_query.update(contact.dict(), synchronize_session=False)
    db.commit()
    db.refresh(updated_contact)
    return create_contactResponse(updated_contact)


# Updating Patch Contact
@app.patch("/contacts/{id}", response_model=schemas.ContactResponse)
def update_contact(id: int, contact: schemas.UpdateContact, db: Session = Depends(get_db)):

    contact_query = db.query(models.Contact).filter(models.Contact.contact_id == id)
    updated_contact = contact_query.first()

    if updated_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found") 
    
    if contact.phone_number:
        is_valid_number(contact.phone_number)

    # Create a dictionary to store the attribute updates
    attribute_updates = update_attributes(contact)    
    # Update the contact attributes with the dictionary of updates
    contact_query.update(attribute_updates, synchronize_session=False)

    db.commit()
    db.refresh(updated_contact)
    return create_contactResponse(updated_contact)


# Deleting Contact
@app.delete("/contacts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(id: int, db: Session = Depends(get_db)):

    contact = db.query(models.Contact).filter(models.Contact.contact_id == id)

    if contact.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")
    
    contact.delete(synchronize_session=False)
    db.commit()
    # Not supposed to return anything


# update since last hangout to current time stamp
@app.patch("/contacts/{id}/linked", response_model=schemas.ContactResponse)
def update_last_hangout(id: int, db: Session = Depends(get_db)):

    contact_query = db.query(models.Contact).filter(models.Contact.contact_id == id)
    contact = contact_query.first()

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")
    
    contact.date_last_hangout = datetime.utcnow()

    db.commit()
    db.refresh(contact)
    return create_contactResponse(contact)
