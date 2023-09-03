from fastapi import FastAPI, Depends,APIRouter,Response, HTTPException
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.routes import admin_routes, doctor_routes, patient_routes, appointment_routes
from app.models.user_connection import UserConnection
from jose import AdminSchema
from passlib.context import CryptContext
from datetime import datetime, timedelta
conn = UserConnection()

app = FastAPI()
auth_scheme = OAuth2PasswordBearer("/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app.title = "Medic Admin App"
app.version ="1.1.0"

# Configuración y middleware aquí
app.add_middleware(
          CORSMiddleware,
          allow_origins=["*"],
          allow_methods=["GET","POST","PUT","DELETE"],
          allow_headers=["Authorization","Content-Type"],
          allow_credentials=True
)
@app.get('/', status_code=HTTP_200_OK,tags=["Root"])
async def root():
     return {'Root API AppMedicAdmin'}


app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])
app.include_router(doctor_routes.router, prefix="/doctors", tags=["Doctors"])
app.include_router(patient_routes.router, prefix="/patients", tags=["Patients"])
app.include_router(appointment_routes.router, prefix="/appointments", tags=["Appointments"])

@app.post('/login', status_code=HTTP_200_OK,tags=["Login"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
     user = auth_user(form_data.username, form_data.password)
     access_token_expires = timedelta(hours=2)
     access_token_jwt = create_token({"sub":user[3]})
     return {"access_token":"que paso","token_type":"bearer"}
# funcion de autenticación que llama a verificar si existe usuario y si la contraseña es correcta
def auth_user(email, password):
     user = get_by_email_user(email)
     hashedPassword=user[10]
     if not user:
          raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate user", 
                headers={"WWW-Authenticate":"Bearer"}) 
     if not verify_pass(password,hashedPassword):
          raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate pass", 
                headers={"WWW-Authenticate":"Bearer"}) 
     return user

#Verifica la contraseña hasheada de la base de datos con la ingresada
def verify_pass(plane_password, hash_password):
     return pwd_context.verify(plane_password, hash_password)

#Verifica que el email corresponde a un usuario cargado en la base de datos
def get_by_email_user(email: str):
     print(email)
     data = conn.read_by_email(email)
     return data