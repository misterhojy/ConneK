from sqlalchemy import Column, BIGINT, String, Integer, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(BIGINT, nullable=True)
    reminder = Column(Integer, nullable=True)
    image = Column(String, nullable=True)
    since_last_hangout = Column(Integer, nullable=False, server_default='0')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


# class User(Base):
#    __tablename__ = "users"
#
#    id = Column(Integer, primary_key=True, nullable=False)
#    phone_number = Column(BIGINT, unique=True, nullable=False)
#    password = Column(String, nullable=False)
#    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
