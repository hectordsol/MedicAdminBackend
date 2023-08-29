from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class AppointmentSchema(BaseModel):
    id: Optional[uuid.UUID]
    start_datetime: datetime
    end_datetime: datetime
    diagnosis: str
    prescription: str
    id_patient: uuid.UUID
    id_doctor: uuid.UUID
    state: str