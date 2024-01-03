from fastapi import FastAPI, status, HTTPException, Depends, APIRouter, BackgroundTasks
from sqlalchemy import and_
from .. import models, schemas, helper, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime
from typing import List


router = APIRouter(
    prefix="/contacts",
    tags=['Contacts']
)

# Creating Contact
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    if contact.phone_number:
        helper.is_valid_number(contact.phone_number)

    new_contact = models.Contact(user_id=current_user.id, **contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return helper.create_contactResponse(new_contact)


# Read Contacts
@router.get("/", response_model=List[schemas.ContactResponse])
def get_contacts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    contacts = db.query(models.Contact).filter(models.Contact.user_id == current_user.id).all() #only the contacts that is made by the user who created

    # Convert the SQLAlchemy Contact models to the Pydantic ContactResponse models
    contact_responses = [
        helper.create_contactResponse(contact) #creating new object of ContactResponse for ever SQL model
        for contact in contacts
    ]

    for contact_response in contact_responses:
        if contact_response.days_since_last_hangout >= contact_response.reminder and contact_response.reminder > 0:
            # notify the front end that it is days after reminder, should be shown in red
            # also send notification to user to hang out
            print(f'Link {contact_response.first_name} {contact_response.last_name}, it\'s been {contact_response.days_since_last_hangout} {"day" if contact_response.days_since_last_hangout == 1 else "days"}!')


    return contact_responses


# Read One Contact
@router.get("/{id}", response_model=schemas.ContactResponse)
def get_contact(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    contact = db.query(models.Contact).filter(and_(models.Contact.user_id == current_user.id, models.Contact.id == id)).first()

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")
    
    return helper.create_contactResponse(contact)


# Updating Replace Contact I DONT THINK YOU NEED THIS
@router.put("/{id}", response_model=schemas.ContactResponse)
def update_contact(id: int, contact: schemas.ContactBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    contact_query = db.query(models.Contact).filter(and_(models.Contact.user_id == current_user.id, models.Contact.id == id))
    updated_contact = contact_query.first()

    if updated_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")  

    if contact.phone_number:
        helper.is_valid_number(contact.phone_number)
    
    contact_query.update(contact.dict(), synchronize_session=False)
    db.commit()
    db.refresh(updated_contact)
    return helper.create_contactResponse(updated_contact)


# Updating Patch Contact
@router.patch("/{id}", response_model=schemas.ContactResponse)
def update_contact(id: int, contact: schemas.UpdateContact, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    contact_query = db.query(models.Contact).filter(and_(models.Contact.user_id == current_user.id, models.Contact.id == id))
    updated_contact = contact_query.first()

    if updated_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found") 
    
    if contact.phone_number:
        helper.is_valid_number(contact.phone_number)

    # Create a dictionary to store the attribute updates
    attribute_updates = helper.update_attributes(contact)    
    # Update the contact attributes with the dictionary of updates
    contact_query.update(attribute_updates, synchronize_session=False)

    db.commit()
    db.refresh(updated_contact)
    return helper.create_contactResponse(updated_contact)


# Deleting Contact
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    contact = db.query(models.Contact).filter(and_(models.Contact.user_id == current_user.id, models.Contact.id == id))

    if contact.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")
    
    contact.delete(synchronize_session=False)
    db.commit()
    # Not supposed to return anything


# update since last hangout to current time stamp
@router.patch("/{id}/linked", response_model=schemas.ContactResponse)
def update_last_hangout(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    contact_query = db.query(models.Contact).filter(and_(models.Contact.user_id == current_user.id, models.Contact.id == id))
    contact = contact_query.first()

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id of {id} not found")
    
    contact.date_last_hangout = datetime.utcnow()

    formatted_date = contact.date_last_hangout.strftime("%m/%d/%y")
    print(f'Linked {contact.first_name} {contact.last_name} on {formatted_date}')

    db.commit()
    db.refresh(contact)
    return helper.create_contactResponse(contact)