from fastapi import APIRouter, Response, Depends,HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from app.models.database_connection import DatabaseConnection
from app.models.appointment_connection import AppointmentConnection
from app.models.user_connection import UserConnection
from app.schemas.appointment_schema import AppointmentSchema
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
ALGORITHM = "HS256"
SECRET_KEY = "e97965045c7df14cb4d5760371e7325104a8f33ad5d00c0a506d6fb09d0047db"
router = APIRouter()
db_conn = DatabaseConnection()
user_conn = UserConnection(db_conn.get_connection())
apmt_conn = AppointmentConnection(db_conn.get_connection())

auth_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# auth_scheme = OAuth2PasswordBearer("/login")

def get_user_current(token: str = Depends(auth_scheme)):
     try:
          token_decode = jwt.decode(token,key=SECRET_KEY,algorithms=[ALGORITHM])
          id_user = token_decode.get("id")
          # print(id_user)
          if id_user == None:
               raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not valid 1", 
                    headers={"WWW-Authenticate":"Bearer"}) 
     except JWTError:
          raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not valid ", 
               headers={"WWW-Authenticate":"Bearer"})
     user = user_conn.read_one(id_user)
     # print(user)
     if not user:
          raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not valid 3", 
               headers={"WWW-Authenticate":"Bearer"})
     return id_user

@router.get('/', status_code=HTTP_200_OK,tags=["Appointments"])
async def get_appointments():
     items=[]
     for data in apmt_conn.read_all():
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
async def create_appointment(appointment: AppointmentSchema):
    data=appointment.dict()
    print(data)
    apmt_conn.write(data)
    return Response(status_code=HTTP_201_CREATED)


@router.get("/{id}", status_code=HTTP_200_OK,tags=["Appointments"])
async def get_one_appointment(id: str):
     dictionary = {}
     data = apmt_conn.read_one(id)
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
async def update_one_appointment(appointment: AppointmentSchema, id:str):
    data=appointment.dict()
    data["id"] = id
    apmt_conn.update_one(data)
    return Response(status_code=HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Appointments"])
async def delete_one_appointment(id: str):
     apmt_conn.delete_one(id)
     return Response(status_code=HTTP_204_NO_CONTENT)

@router.get("/calendar/", status_code=HTTP_200_OK,tags=["Medical Appointments Calendar"])
async def get_calendar(init: str, end: str, token: str = Depends(auth_scheme)):
     id = get_user_current(token)
     print(id)
     data = apmt_conn.read_calendar(init, end, id)
     return data

 