from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.routes import admin_routes, doctor_routes, patient_routes, appointment_routes
from starlette.status import HTTP_200_OK

auth_scheme = OAuth2PasswordBearer("/login")
app = FastAPI()
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
     print(form_data.username, form_data.password)
     return {"access_token":"RootAPI","token_type":"bearer"}
     # return "login"