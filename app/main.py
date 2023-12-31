from fastapi import FastAPI, Depends,APIRouter,Response, HTTPException, Request
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.routes import admin_routes, doctor_routes, patient_routes, appointment_routes
from app.models.user_connection import UserConnection
from jose import jwt
from typing import Union
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.schemas.user_schema import blacklisted_tokens

ALGORITHM = "HS256"
SECRET_KEY = "e97965045c7df14cb4d5760371e7325104a8f33ad5d00c0a506d6fb09d0047db"

user_conn = UserConnection("main_inicio")
user_conn.close_connection("main_inicio")

app = FastAPI()
auth_scheme = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app.title = "Medic Admin App"
app.version ="1.1.0"
origins = [
    r"http://.%2A/.localhost/.com:.*",
]
# Configuración y middleware aquí
app.add_middleware(
          CORSMiddleware,
          allow_origins=["*"],
          allow_methods=["*"],
          allow_headers=["*"],
          allow_credentials=True
)
# allow_headers=["Authorization","Content-Type"],
@app.get('/', status_code=HTTP_200_OK,tags=["Root"])
async def root():
     return {'Root API AppMedicAdmin'}

app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])
app.include_router(doctor_routes.router, prefix="/doctors", tags=["Doctors"])
app.include_router(patient_routes.router, prefix="/patients", tags=["Patients"])
app.include_router(appointment_routes.router, prefix="/appointments", tags=["Appointments"])


#Middleware para verificar, tiene que estar antes de la ruta que lo llama
# def verify_token_in_blacklist(token: str = Depends(auth_scheme)):
#     print("verificando", token)
#     if token in blacklisted_tokens:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token has been revoked",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

@app.post('/login', status_code=HTTP_200_OK,tags=["Login"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
     user = auth_user(form_data.username, form_data.password)
     access_token_expires = timedelta(hours=2)
     access_token_jwt = create_token({"id":user[0],"sub": user[1]+" "+user[2]}, access_token_expires)
     objeto = {}
     objeto["id"] = user[0]
     objeto["first_name"] = user[1]
     objeto["last_name"] = user[2]
     objeto["email"] = user[3]
     return {"user":objeto,"access_token":access_token_jwt,"token_type":"bearer"}

# funcion de autenticación que llama a verificar si existe usuario y si la contraseña es correcta
def auth_user(email, password):
     user = get_by_email_user(email)
     if not user:
          raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate user", 
                headers={"WWW-Authenticate":"Bearer"})
     hashedPassword=user[4]
     if not verify_pass(password,hashedPassword):
          raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate pass", 
                headers={"WWW-Authenticate":"Bearer"})
     return user

#Verifica la contraseña hasheada de la base de datos con la ingresada
def verify_pass(plane_password, hash_password):
     return pwd_context.verify(plane_password, hash_password)

#Verifica que el email corresponde a un usuario cargado en la base de datos
def get_by_email_user(email: str):
     # print(email)
     user_conn.__init__()
     data = user_conn.read_by_email(email)
     user_conn.close_connection()
     return data

def create_token(data: dict, time_expires: Union[datetime,None] = None):
     data_copy = data.copy()
     if time_expires is None:
          expires = datetime.utcnow() + timedelta(hours=1)
     else:
          expires = datetime.utcnow() + time_expires
     data_copy.update({"exp":expires})
     token_jwt = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
     return token_jwt



def revoke_token(token: str):
    blacklisted_tokens.add(token)

@app.post('/logout', tags=["Logout"])
async def logout(token: str = Depends(auth_scheme)):
    revoke_token(token)
    return {"message": "Logout successful"}
