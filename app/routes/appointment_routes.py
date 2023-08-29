from fastapi import APIRouter, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.models.appointment_connection import AppointmentConnection
from app.schemas.appointment_schema import AppointmentSchema

router = APIRouter()
conn = AppointmentConnection()

@router.get('/', status_code=HTTP_200_OK,tags=["Appointments"])
async def get_users():
     items=[]
     for data in conn.read_all():
          dictionary = {}
          dictionary["id"] = data[0]
          dictionary["start_datetime"] = data[1]
          dictionary["end_datetime"] = data[2]
          dictionary["diagnosis"] = data[3]
          dictionary["prescription"] = data[4]
          dictionary["id_patient"] = data[5]
          dictionary["id_doctor"] = data[6]
          dictionary["state"] = data[7]
          items.append(dictionary)
     return items

@router.post("/", status_code=HTTP_201_CREATED,tags=["Appointments"])
async def create_user(appointment: AppointmentSchema):
    data=appointment.dict()
    print(appointment)
    conn.write(appointment)
    return Response(status_code=HTTP_201_CREATED)


@router.get("/{id}", status_code=HTTP_200_OK,tags=["Appointments"])
async def get_one(id: str):
     dictionary = {}
     data = conn.read_one(id)
     dictionary["id"] = data[0]
     dictionary["start_datetime"] = data[1]
     dictionary["end_datetime"] = data[2]
     dictionary["diagnosis"] = data[3]
     dictionary["prescription"] = data[4]
     dictionary["id_patient"] = data[5]
     dictionary["id_doctor"] = data[6]
     dictionary["state"] = data[7]
     return data

@router.put("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Appointments"])
async def update_one(appointment: AppointmentSchema, id:str):
    data=appointment.dict()
    data["id"] = id
    conn.update_one(data)
    return Response(status_code=HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Appointments"])
async def delete_one(id: str):
     conn.delete_one(id)
     return Response(status_code=HTTP_204_NO_CONTENT)