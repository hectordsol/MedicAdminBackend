from fastapi import APIRouter, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from app.models.user_connection import UserConnection
from app.schemas.user_schema import AdminSchema

router = APIRouter()
conn = UserConnection()

@router.get('/', status_code=HTTP_200_OK,tags=["Admin"])
async def get_admins():
     items=[]
     for data in conn.read_all("admin"):
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
          dictionary["user_type"] = data[13]
          items.append(dictionary)
     return items

@router.post("/", status_code=HTTP_201_CREATED,tags=["Admin"])
async def create_admin(user: AdminSchema):
    data=user.dict()
    data["user_type"] = "admin"
    data["health_insurance"] = ""
    data["specialty"] = ""
    print(data)
    conn.write(data)
    return Response(status_code=HTTP_201_CREATED)


@router.get("/{id}", status_code=HTTP_200_OK,tags=["Admin"])
async def get_one_admin(id: str):
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
     dictionary["user_type"] = data[13]
     return data

@router.put("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Admin"])
async def update_one_admin(user: AdminSchema, id:str):
    data=user.dict()
    data["id"] = id
    conn.update_one(data)
    return Response(status_code=HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Admin"])
async def delete_one_admin(id: str):
     conn.delete_one(id)
     return Response(status_code=HTTP_204_NO_CONTENT)
