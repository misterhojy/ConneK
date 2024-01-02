from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas, helper
from .database import engine, get_db
from .routers import contact, user, auth


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


app.include_router(contact.router)
app.include_router(user.router)
app.include_router(auth.router)
