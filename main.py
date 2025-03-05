from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import authentication_routers as atr, users_router as ur

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"], 
    allow_headers=["*"],  # Permite todos los encabezados, cambia según tus necesidades
)
app.include_router(atr.router)
app.include_router(ur.router)