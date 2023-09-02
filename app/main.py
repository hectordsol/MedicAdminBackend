from fastapi import FastAPI, Depends,APIRouter,Response, HTTPException
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.routes import admin_routes, doctor_routes, patient_routes, appointment_routes
from app.models.user_connection import UserConnection
from app.schemas.user_schema import AdminSchema
from passlib.context import CryptContext
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
     auth_user(form_data.username, form_data.password)
     # hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
     # data["password"] = hashed_password.decode('utf-8')
     # return Response(status_code=HTTP_200_OK)

     return {"access_token":"que paso","token_type":"bearer"}
   
def auth_user(email, password):
     user = get_by_email_user(email)
     print(user)
     if not user:
          raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate user", 
                headers={"WWW-Authenticate":"Bearer"}) 
     if not verify_pass(password):
          raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate pass", 
                headers={"WWW-Authenticate":"Bearer"}) 
     return user

def verify_pass(plane_password, hash_password):
     return pwd_context.verify(plane_password, hash_password)

def get_by_email_user(email: str):
     print(email)
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