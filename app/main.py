from fastapi import FastAPI, status, HTTPException, Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from typing import List

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
def create_contact(contact: schemas.CreateContact, db: Session = Depends(get_db)):
    #using SQLAlchemy

    if contact.phone_number:
        # validate phone number
        pass

    new_contact = models.Contact(**contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact



# Read Contacts
@app.get("/contacts", response_model=List[schemas.ContactResponse])
def get_contacts(db: Session = Depends(get_db)):

    contacts = db.query(models.Contact).all()
    return contacts



# Read One Contact
@app.get("/contacts/{id}", response_model=schemas.ContactResponse)
def get_contact(id: int, db: Session = Depends(get_db)):

    #cursor.execute("""SELECT * FROM contacts WHERE id = %s""", (str(id),))
    
    contact = db.query(models.Contact).filter(models.Contact.id == id).first()

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")
    
    return contact



# Updating Replace Contact 
@app.put("/contacts/{id}", response_model=schemas.ContactResponse)
def update_contact(id: int, contact: schemas.CreateContact, db: Session = Depends(get_db)):

    contact_query = db.query(models.Contact).filter(models.Contact.id == id)
    updated_contact = contact_query.first()

    if updated_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")  
    
    if contact.phone_number:
        # validate phone number
        pass
    
    contact_query.update(contact.dict(), synchronize_session=False)
    db.commit()
    return contact_query.first()



# Updating Patch Contact
@app.patch("/contacts/{id}", response_model=schemas.ContactResponse)
def update_contact(id: int, contact: schemas.UpdateContact, db: Session = Depends(get_db)):

    contact_query = db.query(models.Contact).filter(models.Contact.id == id)
    updated_contact = contact_query.first()

    if updated_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found") 
    
    if contact.phone_number:
        # validate phone number
        pass

    # Create a dictionary to store the attribute updates
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

    # Update the contact attributes with the dictionary of updates
    contact_query.update(attribute_updates, synchronize_session=False)

    db.commit()
    db.refresh(updated_contact)
    return updated_contact


# Deleting Contact
@app.delete("/contacts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(id: int, db: Session = Depends(get_db)):

    #cursor.execute("""DELETE FROM contacts WHERE id = %s RETURNING *""", (str(id),))

    contact = db.query(models.Contact).filter(models.Contact.id == id)

    if contact.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")
    
    contact.delete(synchronize_session=False)
    db.commit()

       
# Creating Contact
#@app.post("/users", status_code=status.HTTP_201_CREATED)
#def create_contact(user: schemas.CreateUser, db: Session = Depends(get_db)):
#
#    new_user = models.User(**user.dict())
#    db.add(new_user)
#    db.commit()
#    db.refresh(new_user)
#
#    return new_user