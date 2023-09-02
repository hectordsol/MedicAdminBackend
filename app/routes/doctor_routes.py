from fastapi import APIRouter, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from app.models.user_connection import UserConnection
from app.schemas.user_schema import DoctorSchema
# from passlib.context import CryptContext
import bcrypt

router = APIRouter()
conn = UserConnection()

@router.get('/', status_code=HTTP_200_OK,tags=["Doctors"])
async def get_doctors():
     items=[]
     for data in conn.read_all("doctor"):
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
     return items

@router.post("/", status_code=HTTP_201_CREATED,tags=["Doctors"])
async def create_doctor(user: DoctorSchema):
    data=user.dict()
    data["user_type"] = "doctor"
    data["health_insurance"] = ""
    # Hash de la contraseña antes de guardarla
    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
    data["password"] = hashed_password.decode('utf-8')
    print(data)
    conn.write(data)
    return Response(status_code=HTTP_201_CREATED)


@router.get("/{id}", status_code=HTTP_200_OK,tags=["Doctors"])
async def get_one_doctor(id: str):
     dictionary = {}
     data = conn.read_one(id)
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
     return data

@router.put("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Doctors"])
async def update_one_doctor(user: DoctorSchema, id:str):
    data=user.dict()
    data["id"] = id
    conn.update_one(data)
    return Response(status_code=HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Doctors"])
async def delete_one_doctor(id: str):
     conn.delete_one(id)
     return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/usermail", status_code=HTTP_200_OK,tags=["Doctors"])
async def get_by_email_doctor(email: str):
     dictionary = {}
     data = conn.read_by_email(email)
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
     return data
