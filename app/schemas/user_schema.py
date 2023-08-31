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
    date_of_birth: date
    gender: str
    # user_type: str

class AdminSchema(UserSchema):
    password: str

class DoctorSchema(AdminSchema):
    specialty: str

class PatientSchema(UserSchema):
    health_insurance: str
