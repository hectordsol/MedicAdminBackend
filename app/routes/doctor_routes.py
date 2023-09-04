from fastapi import APIRouter, Response
# from app.models.appointment_connection import AppointmentConnection
from app.models.user_connection import UserConnection

from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from app.schemas.user_schema import DoctorSchema
import bcrypt

router = APIRouter()

user_conn = UserConnection("doctor_routes_inicio")
user_conn.close_connection("doctor_routes_inicio")


@router.get('/', status_code=HTTP_200_OK,tags=["Doctors"])
async def get_doctors():
     items=[]
     user_conn.__init__()
     for data in user_conn.read_all("doctor"):
          dictionary = {}
          dictionary["id"] = data[0]
          dictionary["first_name"] = data[1]
          dictionary["last_name"] = data[2]
          dictionary["email"] = data[3]
          dictionary["address"] = data[4]
          dictionary["city"] = data[5]
          dictionary["country"] = data[6]
          dictionary["phone"] = data[7]
          dictionary["date_of_birth"] = data[8]
          dictionary["gender"] = data[9]
          dictionary["password"] = data[10]
          dictionary["specialty"] = data[11]
          dictionary["user_type"] = data[13]
          items.append(dictionary)
     user_conn.close_connection()
     return items

@router.post("/", status_code=HTTP_201_CREATED,tags=["Doctors"])
async def create_doctor(user: DoctorSchema):
    data=user.dict()
    data["user_type"] = "doctor"
    data["health_insurance"] = ""
    # Hash de la contraseña antes de guardarla
    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
    data["password"] = hashed_password.decode('utf-8')
    user_conn.__init__()
    user_conn.write(data)
    user_conn.close_connection()
    return Response(status_code=HTTP_201_CREATED)


@router.get("/{id}", status_code=HTTP_200_OK,tags=["Doctors"])
async def get_one_doctor(id: str):
     dictionary = {}
     user_conn.__init__()
     data = user_conn.read_one(id)
     dictionary["id"] = data[0]
     dictionary["first_name"] = data[1]
     dictionary["last_name"] = data[2]
     dictionary["email"] = data[3]
     dictionary["address"] = data[4]
     dictionary["city"] = data[5]
     dictionary["country"] = data[6]
     dictionary["phone"] = data[7]
     dictionary["date_of_birth"] = data[8]
     dictionary["gender"] = data[9]
     dictionary["password"] = data[10]
     dictionary["specialty"] = data[11]
     dictionary["user_type"] = data[13]
     user_conn.close_connection()
     return data

@router.put("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Doctors"])
async def update_one_doctor(user: DoctorSchema, id:str):
    data=user.dict()
    data["id"] = id
    data["user_type"] = "doctor"
    data["health_insurance"] = ""
    # Hash de la contraseña antes de guardarla
    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
    data["password"] = hashed_password.decode('utf-8')
    print(data)
    user_conn.__init__()
    user_conn.update_one(data)
    user_conn.close_connection()
    return Response(status_code=HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Doctors"])
async def delete_one_doctor(id: str):
     user_conn.__init__()
     user_conn.delete_one(id)
     user_conn.close_connection()
     return Response(status_code=HTTP_204_NO_CONTENT)
