from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class AppointmentSchema(BaseModel):
    id: Optional[uuid.UUID]
    start_datetime: datetime
    end_datetime: datetime
    diagnosis: Optional[str]
    prescription: Optional[str]
    id_patient: str
    id_doctor: str
    state: str