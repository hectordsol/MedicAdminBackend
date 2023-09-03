from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from app.models.database_connection import DatabaseConnection
from app.models.user_connection import UserConnection
from app.schemas.user_schema import PatientSchema

auth_scheme = OAuth2PasswordBearer(tokenUrl="/login")

router = APIRouter()
db_conn = DatabaseConnection()
user_conn = UserConnection(db_conn.get_connection())

@router.get('/', status_code=HTTP_200_OK,tags=["Patients"])
async def get_patients(token: str = Depends(auth_scheme)):
     items=[]
     for data in user_conn.read_all("patient"):
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
          dictionary["health_insurance"] = data[12]
          dictionary["user_type"] = data[13]
          items.append(dictionary)
     return items

@router.post("/", status_code=HTTP_201_CREATED,tags=["Patients"])
async def create_patient(user: PatientSchema):
    data=user.dict()
    data["user_type"] = "patient"
    data["specialty"] = ""
    data["password"] = ""
    print(data)
    user_conn.write(data)
    return Response(status_code=HTTP_201_CREATED)


@router.get("/{id}", status_code=HTTP_200_OK,tags=["Patients"])
async def get_one_patient(id: str):
     dictionary = {}
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
     dictionary["health_insurance"] = data[12]
     dictionary["user_type"] = data[13]
     return data

@router.put("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Patients"])
async def update_one_patient(user: PatientSchema, id:str):
    data=user.dict()
    data["id"] = id
    user_conn.update_one(data)
    return Response(status_code=HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Patients"])
async def delete_one_patient(id: str):
     user_conn.delete_one(id)
     return Response(status_code=HTTP_204_NO_CONTENT)
