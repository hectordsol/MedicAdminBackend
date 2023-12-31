from fastapi import APIRouter, Response, Depends,HTTPException, status
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
import uuid
from app.models.appointment_connection import AppointmentConnection
from app.models.user_connection import UserConnection
from app.schemas.appointment_schema import AppointmentSchema
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.schemas.user_schema import blacklisted_tokens


ALGORITHM = "HS256"
SECRET_KEY = "e97965045c7df14cb4d5760371e7325104a8f33ad5d00c0a506d6fb09d0047db"
router = APIRouter()
# db_conn = DatabaseConnection("appointment_routes")
# db_conn.close_connection("appointment_routes")
user_conn = UserConnection("user_appointment_routes")
user_conn.close_connection("user_appointment_routes")
apmt_conn = AppointmentConnection("apmt_appintment_routes")
apmt_conn.close_connection("apmt_appintment_routes")

auth_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# auth_scheme = OAuth2PasswordBearer("/login")

async def is_valid_id(id):
    try:
        val = uuid.UUID(id,version=4)
        return str(val) == id
    except ValueError:
        return False

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
     apmt_conn.__init__()
     user = user_conn.read_one(id_user)
     apmt_conn.close_connection()
     # print(user)
     if not user:
          raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not valid 3", 
               headers={"WWW-Authenticate":"Bearer"})
     return id_user

@router.get('/', status_code=HTTP_200_OK,tags=["Appointments"])
async def get_appointments():
     items=[]
     apmt_conn.__init__()
     for data in apmt_conn.read_all():
          dictionary = {}
          dictionary["id"] = data[0]
          dictionary["start_datetime"] = data[1]
          dictionary["end_datetime"] = data[2]
          dictionary["diagnosis"] = data[3]
          dictionary["prescription"] = data[4]
          dictionary["id_patient"] = data[5]
          dictionary["id_doctor"] = data[6]
          dictionary["patient_first_name"] = data[7]
          dictionary["patient_last_name"] = data[8]
          dictionary["doctor_first_name"] = data[9]
          dictionary["doctor_last_name"] = data[10]
          dictionary["state"] = data[11]
          items.append(dictionary)
     apmt_conn.close_connection()
     return items

@router.post("/", status_code=HTTP_201_CREATED,tags=["Appointments"])
async def create_appointment(appointment: AppointmentSchema):
     data=appointment.dict()
     data["state"]="reserved"
     print(data)
     apmt_conn.__init__()
     # print(data["id_doctor"])
     # ver = apmt_conn.check_repeat(data["id_doctor"])
     # print(ver)
     apmt_conn.write(data)
     apmt_conn.close_connection()
     return Response(status_code=HTTP_201_CREATED)


@router.get("/{id}", status_code=HTTP_200_OK,tags=["Appointments"])
async def get_one_appointment(id: str):
     if not await is_valid_id(id):
        raise HTTPException(HTTP_400_BAD_REQUEST, "Invalid id format")
     dictionary = {}
     apmt_conn.__init__()
     data = apmt_conn.read_one(id)
     # dictionary["id"] = data[0]
     dictionary["start_datetime"] = data[0]
     dictionary["end_datetime"] = data[1]
     dictionary["diagnosis"] = data[2]
     dictionary["prescription"] = data[3]
     dictionary["state"] = data[4]
     dictionary["id_patient"] = data[5]
     dictionary["patient_first_name"] = data[6]
     dictionary["patient_last_name"] = data[7]
     dictionary["id_doctor"] = data[8]
     dictionary["doctor_first_name"] = data[9]
     dictionary["doctor_last_name"] = data[10]
     apmt_conn.close_connection()
     return dictionary

@router.put("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Appointments"])
async def update_one_appointment(appointment: AppointmentSchema, id:str):
    data=appointment.dict()
    data["id"] = id
    apmt_conn.__init__()
    apmt_conn.update_one(data)
    apmt_conn.close_connection()
    return Response(status_code=HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Appointments"])
async def delete_one_appointment(id: str):
     apmt_conn.__init__()
     apmt_conn.delete_one(id)
     apmt_conn.close_connection()
     return Response(status_code=HTTP_204_NO_CONTENT)
#Middleware para verificar, tiene que estar antes de la ruta que lo llama
def verify_token_in_blacklist(token: str = Depends(auth_scheme)):
#     print("verificando", token)
    if token in blacklisted_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/calendar/{id_doctor}", status_code=HTTP_200_OK,tags=["Medical Appointments Calendar"])
# async def get_calendar(init: str, end: str,token: dict = Depends(verify_token_in_blacklist)):
async def get_calendar(id_doctor:str, init: str, end: str):

     # id = get_user_current(token)
     user_conn.__init__()
     user = user_conn.read_one(id_doctor)
     user_conn.close_connection()
     if not user:
          raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Doctor not found")
     apmt_conn.__init__()
     items = []
     for data in apmt_conn.read_calendar(id_doctor,init, end ):
          json = {}
          json["id_appointment"] = data[0]
          json["start_datetime"] = data[1]
          json["end_datetime"] = data[2]
          json["status"] = data[3]
          json["id_patient"] = data[4]
          json["fist_name"] = data[5]
          json["last_name"] = data[6]
          items.append(json)
     apmt_conn.close_connection()
     return items


