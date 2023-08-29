from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user_routes, appointment_routes
from starlette.status import HTTP_200_OK

app = FastAPI()
app.title = "Medic Admin App"
app.version ="1.0.0"

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

app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(appointment_routes.router, prefix="/appointments", tags=["Appointments"])
