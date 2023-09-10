from fastapi import APIRouter, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from app.models.database_connection import DatabaseConnection
from app.models.user_connection import UserConnection
from app.schemas.user_schema import AdminSchema
import bcrypt
router = APIRouter()
# db_conn = UserConnection("admin_routes")
# db_conn.close_connection("admin_routes")

user_conn = UserConnection("user_admin_routes")
user_conn.close_connection("user_admin_routes")

@router.get('/', status_code=HTTP_200_OK,tags=["Admin"])
async def get_admins():
     items=[]
     user_conn.__init__()
     for data in user_conn.read_all("admin"):
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
          dictionary["dni"] = data[14]
          items.append(dictionary)
     user_conn.close_connection("admin_routes_read_all")
     return items

@router.post("/", status_code=HTTP_201_CREATED,tags=["Admin"])
async def create_admin(user: AdminSchema):
    data=user.dict()
    data["user_type"] = "admin"
    data["health_insurance"] = ""
    data["specialty"] = ""
    # Hash de la contraseña antes de guardarla
    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
    data["password"] = hashed_password.decode('utf-8')
    print(data)
    user_conn.__init__()
    user_conn.write(data)
    user_conn.close_connection("admin_routes_create")
    return Response(status_code=HTTP_201_CREATED)


@router.get("/{id}", status_code=HTTP_200_OK,tags=["Admin"])
async def get_one_admin(id: str):
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
     dictionary["user_type"] = data[13]
     dictionary["dni"] = data[14]
     user_conn.close_connection("admin_routes_get_one_id")
     return data

@router.put("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Admin"])
async def update_one_admin(user: AdminSchema, id:str):
    data=user.dict()
    data["id"] = id
    data["specialty"] = ""
    data["health_insurance"] =""
    data["user_type"] ="admin"
    # Hash de la contraseña antes de guardarla
    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
    data["password"] = hashed_password.decode('utf-8')
    print(data)
    user_conn.__init__()
    user_conn.update_one(data)
    user_conn.close_connection()
    return Response(status_code=HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT,tags=["Admin"])
async def delete_one_admin(id: str):
     user_conn.__init__()
     user_conn.delete_one(id)
     user_conn.close_connection("admin_routes_delete_one")
     return Response(status_code=HTTP_204_NO_CONTENT)

