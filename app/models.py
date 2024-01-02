from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Contact(Base):
    __tablename__ = "contacts"

    contact_id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    reminder = Column(Integer, nullable=True)
    image = Column(String, nullable=True)
    date_last_hangout = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    # function for computing days since last hangout:
    def days_since_last_hangout(self):

        now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
        time_difference = now_utc - self.date_last_hangout
        
        if time_difference.days < 0:
            return 0 
        return time_difference.days
    

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
