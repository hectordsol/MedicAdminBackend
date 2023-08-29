from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

class UserSchema(BaseModel):
    id:Optional[uuid.UUID]
    first_name: str
    last_name: str
    email:str
    address:Optional[str]
    city:Optional[str]
    country:Optional[str]
    phone:Optional[str]
    password: Optional[str]
    date_of_birth: date
    gender: str
    specialty: str
    health_insurance: str
    password: Optional[str]
    user_type: str
