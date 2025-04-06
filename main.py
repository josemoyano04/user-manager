from fastapi import FastAPI
from utils.env_loader import EnvManager
from fastapi.middleware.cors import CORSMiddleware
from adapters.adapter_db_conn_libsql import AdapterDBConnLibsqlClient
from routers import authentication_routers as atr, users_router as ur, recovery_password_routers as rpr

#====================APP====================
app = FastAPI(
    title= "User Manager API", 
    description= "API for user management, including authentication, registration, and password recovery.", 
    version= "0.2.0",
    contact= {
        "name": "Jose Moyano",
        "url": "http://www.github.com/josemoyano04",
        "email": "josemoyano059@gmail.com",
    })

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"], 
    allow_headers=["*"]
)
app.include_router(atr.router)
app.include_router(ur.router)
app.include_router(rpr.router)