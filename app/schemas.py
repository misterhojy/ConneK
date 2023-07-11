from pydantic import BaseModel
from typing import Optional

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